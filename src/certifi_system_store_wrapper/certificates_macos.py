# Copyright (c) 2025 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .logger import logger
from .certificates import split_certificates

import subprocess


def get_system_certificates_macos() -> list:
    """
    Retrieve system CA certificates from macOS keychains.

    This function uses the 'security' command to export certificates from both
    the SystemRootCertificates and System keychains, splits them into individual
    certificates, and returns a combined list.

    Returns:
        list: A list of certificate strings found on the macOS system.
    """
    try:
        # Export certificates from the SystemRootCertificates keychain
        r1 = subprocess.run(['security', 'export', '-t', 'certs', '-f', 'pemseq', '-k',
                             '/System/Library/Keychains/SystemRootCertificates.keychain'],
                            check=True, stdout=subprocess.PIPE)
        c1 = split_certificates(r1.stdout.decode('ascii'))
        logger.info(f'Got {len(c1)} CAs from macOS root CA.')

        # Export certificates from the System keychain
        r2 = subprocess.run(['security', 'export', '-t', 'certs', '-f', 'pemseq', '-k',
                             '/Library/Keychains/System.keychain'],
                            check=True, stdout=subprocess.PIPE)
        c2 = split_certificates(r2.stdout.decode('ascii'))
        logger.info(f'Got {len(c2)} CAs from macOS system CA.')

        # Combine and deduplicate certificates from both sources
        return list(set(c1 + c2))
    except Exception as e:
        # If any error occurs, return an empty list
        logger.error(f'Failed to get macOS system certificates: {e}')
        return []
