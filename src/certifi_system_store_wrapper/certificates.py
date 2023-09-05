# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .logger import logger

import glob
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
        from .certificates_linux import get_system_certificates_linux
        system_certificates = get_system_certificates_linux()
    if systemname == 'Windows':
        from .certificates_win import get_system_certificates_win
        system_certificates = get_system_certificates_win()
    if systemname == 'Darwin':
        from .certificates_macos import get_system_certificates_macos
        system_certificates = get_system_certificates_macos()
    logger.info(f'Got {len(system_certificates)} CAs from system.')
    return system_certificates


def get_ssl_certificates() -> list:
    try:
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.load_default_certs()
        certs = [ssl.DER_cert_to_PEM_cert(der_cert).strip(
        ) for der_cert in ssl_context.get_ca_certs(binary_form=True)]
        logger.info(f'Got {len(certs)} CAs from SSL.')
        return certs
    except:
        return []


def get_certificates() -> list:
    certs = []
    certifi_certs = split_certificates(certifi.contents())
    logger.info(f'Got {len(certifi_certs)} CAs from original certifi.')
    certs.append(certifi_certs)
    certs.append(get_system_certificates())
    certs.append(get_ssl_certificates())
    cer_filenames = glob.glob(
        f'{os.path.dirname(__file__)}/**/*.cer', recursive=True)
    cer_filenames += os.environ.get('PYTHON_CERTIFI_CERT_FILES',
                                    '').split(os.pathsep)

    for fn in cer_filenames:
        if os.path.exists(fn):
            with open(fn) as f:
                local_certs = split_certificates(f.read())
                logger.info(f'Got {len(local_certs)} CAs from {fn}.')
                certs.append(local_certs)

    c = []
    for cert in certs:
        c = c + cert
    logger.info(f'Total num of CAs: {len(c)}.')
    r = list(set(c))
    logger.info(f'Total num of de-duplicated CAs: {len(r)}.')
    return r
