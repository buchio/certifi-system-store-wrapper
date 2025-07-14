# certifi-system-store-wrapper
certifiをハックして、システムの信頼ストアとユーザー独自のCAを使用するためのラッパーです。

# 動機

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

# 使い方

インストールするだけで利用することができます。

    pip install certifi-system-store-wrapper

## ユーザー独自の認証局の追加方法

### 環境変数 `PYTHON_CERTIFI_CERT_FILES` を設定する

Linux/macOSでは `:` 区切、Windowsでは `;` 区切でファイルを指定します。

    Windows
    > SET PYTHON_CERTIFI_CERT_FILES=C:\CA\My_Root_CA.cer;C:\CA2\My_Root_CA2.cer
    Linux/macOS
    $ export PYTHON_CERTIFI_CERT_FILES=~/My_Root_CA.cer:~/My_Root_CA2.cer


フルパスで指定した方が良いです。

### ファイルを直接パッケージ内にコピーする

拡張子は `cer` 固定です。複数のファイルに対応しています。

    Windows
    > copy My_Root_CA.cer C:\Python311\lib\site-packages\certifi_system\
    Linux/macOS
    $ copy My_Root_CA.cer ~/.venv/lib/python3.11/site-packages/certifi_system\


# ビルド

ビルドするには、以下のコマンドを実行します。

    pip wheel -w whl --no-deps .


# 他のインストール方法

### 最新のソースからインストールする

    pip install -U git+https://github.com/buchio/certifi-system-store-wrapper.git

### 現在の開発ディレクトリからインストールする

    git clone https://github.com/buchio/certifi-system-store-wrapper
    cd certifi-system-store-wrapper
    pip install -U .

# ログ出力

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

# 制約

- 確認していませんが、PyInstallerなどでバイナリ化した場合には動作しな
  いと思います。回避策もありますので、確認後記述します。
- Python 3.7以降が必要ですが、動作確認はPython 3.8以降でのみ行っています。
  Python 2では間違いなく動作しませんし、サポートの予定もありません。
- 現在はWindows 10、macOS Ventura、Ubuntu 20.04でのみ動作確認しています。
  それ以外のプラットフォームではうまく動作しないと思われます。

# 参考
- https://gitlab.com/alelec/python-certifi-win32
  - これはWindows専用のライブラリで、certifiをフックしてシステムにインストールされている認証局のリストを返すように変更するものです。もはやメンテナンスされていないようですが、Windowsの認証局情報を取得するコードは特に参考になりました。

- https://gitlab.com/alelec/pip-system-certs
  - python-certifi-win32の後継ですが、requestsライブラリを拡張してsslライブラリの認証局情報を使用するようになっています。しかし、requestsに限定されているため、少し使いにくくなっています。

- https://github.com/tiran/certifi-system-store
  - このライブラリとほぼ同じ目的で設計されていますが、残念ながらLinux/FreeBSD専用です。各Linuxディストリビューションの認証局の場所に関する情報は非常に参考になります。
