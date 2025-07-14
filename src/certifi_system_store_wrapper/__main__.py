# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

"""
This module serves as the entry point for the certifi-system-store-wrapper package.

It provides functionality to display information about the certifi-system package,
including its version, the location of its certificate store, and the number of
certificates it contains.
"""

import certifi  # Standard Python package for Mozilla CA Bundle
import certifi_system  # Provides system CA certificates integration


def main() -> None:
    """
    The main function of the script.

    It prints the following information about the certifi-system package:
    - Version of the certifi-system package.
    - Location of the certificate store used by certifi.
    - Number of certificates in the certifi contents.
    """
    # Print the version of certifi-system
    print(f'certifi-system version [{certifi_system.version}]')  # Output the version of certifi-system
    # Print the path to the certificate store used by certifi
    print(f'certifi-system where [{certifi.where()}]')  # Output the path to the certificate store
    # Print the number of certificates in the certifi contents
    print(f'certifi-system contents [{len(certifi.contents())}]')


if __name__ == "__main__":
    # Execute main function if this script is run
    main()
