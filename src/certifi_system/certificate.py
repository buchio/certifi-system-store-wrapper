# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

import os
import platform
import certifi
import re


def split_certificates(text) -> list:
    certificates = []
    cert = []
    in_cert = False
    for l in text.splitlines():
        l = l.strip()
        if re.match('-----BEGIN CERTIFICATE-----', l):
            in_cert = True
            cert.append(l)
        elif re.match('-----END CERTIFICATE-----', l):
            in_cert = False
            cert.append(l)
            certificates.append('\n'.join(cert))
            cert = []
        elif in_cert:
            cert.append(l)
    return certificates


def get_system_certificates() -> list:
    systemname = platform.system()
    system_certificates = []
    if systemname == 'Linux':
        from .certificate_linux import get_system_certificate_linux
        system_certificates = get_system_certificate_linux()
    if systemname == 'Windows':
        from .certificate_win import get_system_certificate_win
        system_certificates = get_system_certificate_win()
    if systemname == 'Darwin':
        from .certificate_macos import get_system_certificate_macos
        system_certificates = get_system_certificate_macos()
    return system_certificates


def get_ssl_certificates() -> list:
    try:
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.load_default_certs()
        return [ssl.DER_cert_to_PEM_cert(der_cert).strip() for der_cert in ssl_context.get_ca_certs(binary_form=True)]
    except:
        return []


def get_certificates() -> list:
    c1 = split_certificates(certifi.contents())
    c2 = get_system_certificates()
    c3 = get_ssl_certificates()
    local_pem_filename = os.path.join(os.path.dirname(__file__), 'local.pem')
    c4 = []
    if os.path.exists(local_pem_filename):
        with open(local_pem_filename) as f:
            c4 = split_certificates(f.read())
    # print(f'Certifi: {len(c1)}')
    # print(f'System:  {len(c2)}')
    # print(f'SSL:     {len(c3)}')
    # print(f'Local:   {len(c4)}')
    # print(f'Total:   {len(c1 + c2 + c3 + c4)}')
    # print(f'Dedup:   {len(set(c1 + c2 + c3 + c4))}')

    return list(set(c1 + c2 + c3 + c4))
