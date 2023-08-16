# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .certificates import split_certificates
import os


def get_system_certificates_linux() -> list:
    contents = ''
    for f in ['/etc/ssl/cert.pem',
              '/etc/pki/tls/cert.pem',
              '/etc/ssl/certs/ca-certificates.crt',
              '/etc/ssl/ca-bundle.pem']:
        if os.path.exists(f):
            with open(f) as f:
                contents += f.read()
    return split_certificates(contents)
