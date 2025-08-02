# certifi-system-store-wrapper
A wrapper for certifi to use the system trust store and user's own CA.

## Motivation

The [certifi](https://pypi.org/project/certifi/) library is often used
in Python to obtain certificate authority information for SSL/TSL
communication, but this library only provides a Mozilla-approved
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

    pip install certifi-system-store-wrapper

### How to add a user's own Certificate Authority

#### Set the environment variable `PYTHON_CERTIFI_CERT_FILES`.

Specify files with `:` separators on Linux/macOS and `;` separators on Windows.

    Windows
    > SET PYTHON_CERTIFI_CERT_FILES=C:\CA\My_Root_CA.cer;C:\CA2\My_Root_CA2.cer
    Linux/macOS
    $ export PYTHON_CERTIFI_CERT_FILES=~/My_Root_CA.cer:~/My_Root_CA2.cer


It is better to specify the full path.

#### Copy the file directly into the package.

The extension is fixed to `cer`. Multiple files are supported.

    Windows
    > copy My_Root_CA.cer C:\Python311\lib\site-packages\certifi_system\
    Linux/macOS
    $ copy My_Root_CA.cer ~/.venv/lib/python3.11/site-packages/certifi_system/


## Build

To build it, exec followings.

    pip wheel -w whl --no-deps .


## Other install method.

### Install from newest source.

    pip install -U git+https://github.com/buchio/certifi-system-store-wrapper.git

### Install from current development directory.

    git clone https://github.com/buchio/certifi-system-store-wrapper
    cd certifi-system-store-wrapper
    pip install -U .

## Log output

Log output can be controlled by environment variables.

- `PYTHON_CERTIFI_LOG_LEVEL`.
  Set to one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
  Default is `WARNING`.

- `PYTHON_CERTIFI_LOG_FILE`.
  Specifies the name of the file to log to.
  Defaults to empty, no file output.

- `PYTHON_CERTIFI_LOG_FILE_LEVEL`.
  Set to one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
  Default is `DEBUG`.

## Architecture

This library hooks into Python's startup process and dynamically wraps the `certifi` functions when `certifi` is imported, enabling the use of the system's certificate store and user-specified certificates.

### Startup Sequence

1.  **Initialization via `.pth` file**:
    When Python starts, it reads the `.pth` file in the `site-packages` directory. This project places a file named `certifi_system_store_wrapper.pth`, which imports the `certifi_system_store_wrapper` module.

2.  **Bootstrap Process**:
    When the `certifi_system_store_wrapper` module is imported, `__init__.py` calls `bootstrap.bootstrap()`.
    `bootstrap.py` wraps the `execsitecustomize` and `execusercustomize` functions of Python's `site` module. This allows registering a hook to wrap `certifi` at the appropriate time in Python's initialization process.

3.  **`certifi` Import Hook**:
    Using the `wrapt.when_imported('certifi')` decorator, the `apply_certifi_patches` function is set to be called when the `certifi` module is imported.

### Certificate Collection and Replacement

1.  **Wrapping `certifi` Functions**:
    The `apply_certifi_patches` function calls `wrapper.wrap_functions`.
    `wrap_functions` replaces the `certifi.where()` and `certifi.contents()` functions with its own functions using `wrapt`.

2.  **Certificate Collection**:
    `wrapper.py` calls `certificates.get_certificates()` to collect certificates from the following sources:
    -   **certifi**: Gets the original certificates from `certifi.contents()`.
    -   **System Store**:
        -   **Windows**: Uses the `wincertstore` library to get certificates from the Windows certificate store.
        -   **macOS**: Exports certificates from the keychain using the `security` command.
        -   **Linux**: Reads certificate files from common paths (e.g., `/etc/ssl/certs/ca-certificates.crt`).
    -   **SSL Module**: Gets certificates using Python's `ssl.create_default_context()`.
    -   **User-specified**: Reads files specified by the `PYTHON_CERTIFI_CERT_FILES` environment variable and `.cer` files in the package directory.

3.  **Temporary File Creation and Replacement**:
    -   Deduplicates all collected certificates and writes them to a temporary file.
    -   The wrapped `certifi.where()` will now return the path to this temporary file.
    -   The wrapped `certifi.contents()` will now return the content of this temporary file.

4.  **Cleanup**:
    Registers `atexit` and signal handlers (`SIGTERM`, `SIGINT`) to ensure the created temporary file is deleted upon Python process termination.

This architecture allows existing code that uses `certifi` to utilize the system's certificate store and user's own certificates without any modifications.

## Restrictions

- I have not checked, but I don't think it will work if it is
  binaryized with PyInstaller or other software. There is a
  workaround, which will be described after confirmation.
- Requires Python 3.7 or later, but we have confirmed that it works only with Python 3.8 or later.
  It definitely does not work with Python 2, and we do not plan to support it.
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
