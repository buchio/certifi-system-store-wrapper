# Copyright (c) 2025 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .certificates import split_certificates
import os


def get_system_certificates_linux() -> list:
    """
    Retrieve system CA certificates from common Linux certificate bundle locations.

    This function searches for certificate bundle files in typical Linux paths,
    reads their contents if they exist, and splits them into individual certificates.

    Returns:
        list: A list of certificate strings found on the system.
    """
    contents = ''
    # List of common certificate bundle file paths on Linux
    for f in ['/etc/ssl/cert.pem',
              '/etc/pki/tls/cert.pem',
              '/etc/ssl/certs/ca-certificates.crt',
              '/etc/ssl/ca-bundle.pem']:
        if os.path.exists(f):
            # Read the certificate file and append its contents
            with open(f) as f:
                contents += f.read()
    # Split the concatenated certificates and return as a list
    return split_certificates(contents)
