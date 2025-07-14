# Copyright (c) 2025 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

import atexit
import os
import signal
import sys
import tempfile
import wrapt

# Store original certifi.where and certifi.contents functions for restoration if needed
certifi_where = None
certifi_contents = None

# Path to the temporary certificate bundle file
cert_file = None


def wrap_where(wrapped, instance, args, kwargs) -> str:
    """
    Wrapper function for certifi.where().
    Returns the path to the temporary certificate bundle file.
    """
    ret = cert_file
    return ret


def wrap_contents(wrapped, instance, args, kwargs) -> str:
    """
    Wrapper function for certifi.contents().
    Returns the contents of the temporary certificate bundle file.
    """
    ret = open(cert_file).read()
    return ret


def _cleanup() -> None:
    """
    Remove the temporary certificate bundle file on exit.
    """
    global cert_file
    if os.path.exists(cert_file):
        os.remove(cert_file)


def _sig_handler(signum, frame) -> None:
    """
    Signal handler to clean up the temporary file on SIGTERM or SIGINT.
    """
    _cleanup()
    sys.exit(1)


def wrap_functions(certifi) -> None:
    """
    Replace certifi.where and certifi.contents with wrappers that use a dynamically
    generated certificate bundle file containing system and user certificates.
    """
    global cert_file
    # Create a temporary file to store the combined certificate bundle
    h, cert_file = tempfile.mkstemp()
    os.close(h)

    # Write all collected certificates to the temporary file
    with open(cert_file, 'w') as f:
        from .certificates import get_certificates
        for cert in get_certificates():
            for l in cert.splitlines():
                print(l, file=f)

    # Register cleanup handlers for process exit and signals
    signal.signal(signal.SIGTERM, _sig_handler)
    signal.signal(signal.SIGINT, _sig_handler)
    atexit.register(_cleanup)

    # Store original certifi functions and apply wrappers
    global certifi_where
    certifi_where = certifi.where
    wrapt.wrap_function_wrapper(certifi, 'where', wrap_where)
    global certifi_contents
    certifi_contents = certifi.contents
    wrapt.wrap_function_wrapper(certifi, 'contents', wrap_contents)
