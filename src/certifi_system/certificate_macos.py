# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .certificate import split_certificates

import subprocess


def get_system_certificate_macos() -> list:
    try:
        r1 = subprocess.run(['security', 'export', '-t', 'certs', '-f', 'pemseq', '-k',
                             '/System/Library/Keychains/SystemRootCertificates.keychain'], check=True, stdout=subprocess.PIPE)
        c1 = split_certificates(r1.stdout.decode('ascii'))
        r2 = subprocess.run(['security', 'export', '-t', 'certs', '-f', 'pemseq', '-k',
                             '/Library/Keychains/System.keychain'], check=True, stdout=subprocess.PIPE)
        c2 = split_certificates(r2.stdout.decode('ascii'))
        return list(set(c1+c2))
    except:
        return []
