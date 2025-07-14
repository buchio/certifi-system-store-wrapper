# Copyright (c) 2025 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .certificates import split_certificates


def get_system_certificates_win() -> list:
    """
    Retrieve system CA certificates from Windows certificate stores.

    This function uses the wincertstore library to access the "CA" and "ROOT"
    certificate stores, extracts certificates for server authentication usage,
    and returns them as a list of PEM-encoded certificate strings.

    Returns:
        list: A list of certificate strings found in the Windows system stores.
    """
    import wincertstore
    pems = []
    # Iterate over both "CA" and "ROOT" certificate stores
    for store_name in ("CA", "ROOT"):
        with wincertstore.CertSystemStore(store_name) as store:
            # Iterate over certificates with SERVER_AUTH usage
            for cert in store.itercerts(usage=wincertstore.SERVER_AUTH):
                try:
                    pem = cert.get_pem()
                    # Decode bytes to ASCII if necessary
                    pem = pem.decode('ascii') if isinstance(pem, bytes) else pem
                    pems.append(pem.strip())
                except:
                    # Ignore certificates that cannot be processed
                    pass

    return pems
