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

現在このライブラリはまだPyPIに登録していませんので、以下の方法でインス
トールする必要があります。


    pip install -U git+https://github.com/buchio/certifi-system-store-wrapper.git


将来PyPIに登録したら、以下の方法でインストールできるようになるはずです。


    pip install -U certifi-system-store-wrapper

## ユーザー独自の認証局の追加方法

### 環境変数 `PYTHON_CERT_FILES` を設定する

Linux/macOSでは `:` 区切、Windowsでは `;` 区切でファイルを指定します。

    Windows
    > SET PYTHON_CERT_FILES=C:\CA\My_Root_CA.cer;C:\CA2\My_Root_CA2.cer
    Linux/macOS
    $ export PYTHON_CERT_FILES=~/My_Root_CA.cer:~/My_Root_CA2.cer


フルパスで指定した方が良いです。

### ファイルを直接パッケージ内にコピーする

拡張子は `cer` 固定です。複数のファイルに対応しています。

    Windows
    > copy My_Root_CA.cer C:\Python311\lib\site-packages\certifi_system\
    Linux/macOS
    $ copy My_Root_CA.cer ~/.venv/lib/python3.11/site-packages/certifi_system/


# 制約

- 確認していませんが、PyInstallerなどでバイナリ化した場合には動作しな
  いと思います。回避策もありますので、確認後記述します。
- Python3.8以降でのみ動作確認しています。Python2では間違いなく動きませ
  んし、サポートの予定もありません。おそらくPython3.6より前では動かな
  いと思います。
- 現在はWindows10、macOS Ventura、Ubuntu20.04でのみ動作確認しています。
  それ以外のプラットフォームではうまく動作しないと思われます。

## 参考
- https://gitlab.com/alelec/python-certifi-win32
  - Windows専用のライブラリですが、これと同じものをLinux/macOSでも使いたい
    というのが今回の開発動機でした。もはやメンテナンスが止まっており、下記の
    pip-system-certsに引き継がれていますが、Windowsの認証局情報取得の方法など
    実装面で非常に参考になりました。

- https://gitlab.com/alelec/pip-system-certs
  - 上記のpython-certifi-win32の後継ですが、pip専用っぽくなっていたり、
    システムからではなくsslの認証曲情報を取得するようになっていたりしています。

- https://github.com/tiran/certifi-system-store
  - こちらもこのライブラリと同じ動機で開発されたものですが、Linux/FreeBSD
    専用だったので今回の用途では少し使いにくいものでした。
    各ディストリビューションでの認証局の保存場所についてまとめて下さっているのは
    非常に有り難かったです。
