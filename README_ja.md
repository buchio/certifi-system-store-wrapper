# certifi-system-store-wrapper
certifiをハックして、システムの信頼ストアとユーザー独自のCAを使用するためのラッパーです。

## 動機

PythonにおいてSSL/TSL通信を行う際に、認証局情報を取得するためによく使
われている[certifi](https://pypi.org/project/certifi/)ライブラリですが、
このライブラリはあくまでMozillaが認定したRoot認証局を提供するもので
あり、それ以上の機能は提供されていません。独自の認証局を追加する方法も
公式には提供されていません。

しかしながら、requestsライブラリがcertifiに依存しているため、結果的に
requestsに依存している多くのライブラリがcertifiを用いて認証局情報を取
得している状況です。

そこで、certifiライブラリを拡張し、certifiが提供している認証局情報に加
えて、システムにインストールされている認証局情報と、さらにはユーザー独
自の認証局情報を取り扱えるようにするラッパーライブラリを作成しました。

本来、このような機能はPython本体に含まれるべきであり、一刻も早くこのよ
うなライブラリが無用になることを願っています。

## 使い方

インストールするだけで利用することができます。

    pip install certifi-system-store-wrapper

### ユーザー独自の認証局の追加方法

#### 環境変数 `PYTHON_CERTIFI_CERT_FILES` を設定する

Linux/macOSでは `:` 区切、Windowsでは `;` 区切でファイルを指定します。

    Windows
    > SET PYTHON_CERTIFI_CERT_FILES=C:\CA\My_Root_CA.cer;C:\CA2\My_Root_CA2.cer
    Linux/macOS
    $ export PYTHON_CERTIFI_CERT_FILES=~/My_Root_CA.cer:~/My_Root_CA2.cer


フルパスで指定した方が良いです。

#### ファイルを直接パッケージ内にコピーする

拡張子は `cer` 固定です。複数のファイルに対応しています。

    Windows
    > copy My_Root_CA.cer C:\Python311\lib\site-packages\certifi_system\
    Linux/macOS
    $ copy My_Root_CA.cer ~/.venv/lib/python3.11/site-packages/certifi_system\


## ビルド

ビルドするには、以下のコマンドを実行します。

    pip wheel -w whl --no-deps .


## 他のインストール方法

### 最新のソースからインストールする

    pip install -U git+https://github.com/buchio/certifi-system-store-wrapper.git

### 現在の開発ディレクトリからインストールする

    git clone https://github.com/buchio/certifi-system-store-wrapper
    cd certifi-system-store-wrapper
    pip install -U .

## ログ出力

環境変数でログ出力を制御することができます。

- `PYTHON_CERTIFI_LOG_LEVEL`
  `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`のいずれかを設定します。
  デフォルトは `WARNING`です。

- `PYTHON_CERTIFI_LOG_FILE`
  ログファイルを記録するファイル名を指定します。
  デフォルトは空で、ファイル出力はしません。

- `PYTHON_CERTIFI_LOG_FILE_LEVEL`
  `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`のいずれかを設定します。
  デフォルトは `DEBUG`です。

## アーキテクチャ

このライブラリは、Pythonの起動プロセスにフックし、`certifi`がインポートされたタイミングで`certifi`の関数を動的にラップすることで、システムの証明書ストアとユーザー指定の証明書を追加できるようにしています。

### 起動シーケンス

1.  **`.pth`ファイルによる初期化**:
    Pythonの起動時に、`site-packages`ディレクトリにある`.pth`ファイルが読み込まれます。このプロジェクトでは`certifi_system_store_wrapper.pth`というファイルが配置され、このファイルが`certifi_system_store_wrapper`モジュールをインポートします。

2.  **ブートストラップ処理**:
    `certifi_system_store_wrapper`モジュールがインポートされると、`__init__.py`が`bootstrap.bootstrap()`を呼び出します。
    `bootstrap.py`は、Pythonの`site`モジュールの`execsitecustomize`と`execusercustomize`関数をラップします。これにより、Pythonの初期化プロセスの適切なタイミングで、`certifi`をラップするためのフックを登録します。

3.  **`certifi`のインポートフック**:
    `wrapt.when_imported('certifi')`デコレータを使い、`certifi`モジュールがインポートされたときに`apply_certifi_patches`関数が呼ばれるように設定します。

### 証明書の収集と置換

1.  **`certifi`関数のラップ**:
    `apply_certifi_patches`関数は、`wrapper.wrap_functions`を呼び出します。
    `wrap_functions`は、`certifi.where()`と`certifi.contents()`関数を`wrapt`を使って独自の関数に置き換えます。

2.  **証明書の収集**:
    `wrapper.py`は、`certificates.get_certificates()`を呼び出して、以下のソースから証明書を収集します。
    -   **certifi**: `certifi.contents()`からオリジナルの証明書を取得します。
    -   **システムストア**:
        -   **Windows**: `wincertstore`ライブラリを使って、Windowsの証明書ストアから証明書を取得します。
        -   **macOS**: `security`コマンドを使って、キーチェーンから証明書をエクスポートします。
        -   **Linux**: 一般的なパス（`/etc/ssl/certs/ca-certificates.crt`など）から証明書ファイルを読み込みます。
    -   **SSLモジュール**: Pythonの`ssl.create_default_context()`を使って証明書を取得します。
    -   **ユーザー指定**: 環境変数`PYTHON_CERTIFI_CERT_FILES`で指定されたファイルや、パッケージディレクトリ内の`.cer`ファイルを読み込みます。

3.  **一時ファイルの作成と置換**:
    -   収集したすべての証明書を重複排除し、一時ファイルに書き込みます。
    -   ラップされた`certifi.where()`は、この一時ファイルのパスを返すようになります。
    -   ラップされた`certifi.contents()`は、この一時ファイルの内容を返すようになります。

4.  **クリーンアップ**:
    `atexit`とシグナルハンドラ（`SIGTERM`, `SIGINT`）を登録し、Pythonプロセスの終了時に作成した一時ファイルを確実に削除します。

このアーキテクチャにより、`certifi`を利用する既存のコードを一切変更することなく、システムの証明書ストアやユーザー独自の証明書を利用できるようになります。

## 制約

- Python 3.7以降が必要ですが、動作確認はPython 3.8以降でのみ行っています。
  Python 2では間違いなく動作しませんし、サポートの予定もありません。
- 現在はWindows 10、macOS Ventura、Ubuntu 20.04でのみ動作確認しています。
  それ以外のプラットフォームではうまく動作しないと思われます。
- PyInstallerなどでバイナリ化した場合には動作しないと思います。

## 参考
- https://gitlab.com/alelec/python-certifi-win32
  - これはWindows専用のライブラリで、certifiをフックしてシステムにインストールされている認証局のリストを返すように変更するものです。もはやメンテナンスされていないようですが、Windowsの認証局情報を取得するコードは特に参考になりました。

- https://gitlab.com/alelec/pip-system-certs
  - python-certifi-win32の後継ですが、requestsライブラリを拡張してsslライブラリの認証局情報を使用するようになっています。しかし、requestsに限定されているため、少し使いにくくなっています。

- https://github.com/tiran/certifi-system-store
  - このライブラリとほぼ同じ目的で設計されていますが、残念ながらLinux/FreeBSD専用です。各Linuxディストリビューションの認証局の場所に関する情報は非常に参考になります。
