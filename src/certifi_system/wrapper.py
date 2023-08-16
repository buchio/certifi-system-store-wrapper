# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

import atexit
import os
import signal
import sys
import tempfile
import wrapt

certifi_where = None
certifi_contents = None

cert_file = None


def wrap_where(wrapped, instance, args, kwargs) -> str:
    ret = cert_file
    return ret


def wrap_contents(wrapped, instance, args, kwargs) -> str:
    ret = open(cert_file).read()
    return ret


def _cleanup() -> None:
    global cert_file
    if os.path.exists(cert_file):
        os.remove(cert_file)


def _sig_handler(signum, frame) -> None:
    _cleanup()
    sys.exit(1)


def wrap_functions(certifi) -> None:

    global cert_file
    h, cert_file = tempfile.mkstemp()
    os.close(h)

    with open(cert_file, 'w') as f:
        from .certificate import get_certificates
        for cert in get_certificates():
            for l in cert.splitlines():
                print(l, file=f)

    signal.signal(signal.SIGTERM, _sig_handler)
    signal.signal(signal.SIGINT, _sig_handler)
    atexit.register(_cleanup)

    global certifi_where
    certifi_where = certifi.where
    wrapt.wrap_function_wrapper(certifi, 'where', wrap_where)
    global certifi_contents
    certifi_contents = certifi.contents
    wrapt.wrap_function_wrapper(certifi, 'contents', wrap_contents)
