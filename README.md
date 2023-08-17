# certifi-system-store-wrapper
A certifi hack to use system trust store and use's own CA.

## Motivation

The [certifi](https://pypi.org/project/certifi/) library is often used
in Python to obtain certificate authority information for SSL/TSL
communication, but this library only provides a Mozzillla-approved
Root certificate authority and does not provide any further
functionality. There is also no official way to add your own
certificate authority.

However, the requests library depends on certifi, and as a result,
many libraries that depend on requests use certifi to obtain
certificate authority information.

Therefore, I have created a wrapper library that extends the certifi
library to handle not only the CA information provided by certifi, but
also the CA information installed on the system and even the user's
own CA information.

Such functionality should be included in Python itself, and I hope
that such a library will be rendered useless as soon as possible.

## Usage

You can use this library simply by installing it.

Currently, this library is not yet registered with PyPI, so it must be
installed in the following way

    pip install -U git+https://github.com/buchio/certifi-system-store-wrapper.git

In the future, once it is registered with PyPI, you should be able to
install it using the following method.

    pip install -U certifi-system-store-wrapper

## How to add a user's own Certificate Authority

### Set the environment variable `PYTHON_CERT_FILES`.

Specify files with `:` separators on Linux/macOS and `;` separators on Windows.

    Windows
    > SET PYTHON_CERT_FILES=C:\CA\My_Root_CA.cer;C:\CA2\My_Root_CA2.cer
    Linux/macOS
    $ export PYTHON_CERT_FILES=~/My_Root_CA.cer:~/My_Root_CA2.cer


It is better to specify the full path.

### Copy the file directly into the package.

The extension is fixed to `cer`. Multiple files are supported.

    Windows
    > copy My_Root_CA.cer C:\Python311\lib\site-packages\certifi_system\
    Linux/macOS
    $ copy My_Root_CA.cer ~/.venv/lib/python3.11/site-packages/certifi_system/


# Restrictions

- I have not checked, but I don't think it will work if it is
  binaryized with PyInstaller or other software. There is a
  workaround, which will be described after confirmation.
- We have confirmed that it works only with Python 3.8 or later; it
  definitely does not work with Python 2, and we do not plan to
  support it. It probably will not work with Python 3.6 or earlier.
- Currently only tested on Windows 10, macOS Ventura, and Ubuntu
  20.04. It is not expected to work well on other platforms.

## References
- https://gitlab.com/alelec/python-certifi-win32
  - This is a Windows-only library that hooks certifi and modifies it
    to return a list of certification authorities installed on the
    system. Although it no longer seems to be maintained, the code to
    retrieve Windows Certificate Authority information was
    particularly helpful.

- https://gitlab.com/alelec/pip-system-certs
  - It extends the requests library to use the certificate authority
    information from the ssl library, which is a successor to
    python-certifi-win32, but it is a bit harder to use because it is
    limited to requests.

- https://github.com/tiran/certifi-system-store
  - It is designed for almost the same purpose as this library, but
    unfortunately it is for Linux/FreeBSD only. The information about
    the location of the certificate authority for each Linux
    distribution is very helpful.
  
  







