# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .certificate import split_certificates


def get_system_certificate_linux() -> list:

    with open('/etc/ssl/certs/ca-certificates.crt') as f:
        return split_certificates(f.read())
