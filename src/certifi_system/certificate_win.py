# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .certificate import split_certificates


def get_system_certificate_win() -> list:
    import wincertstore
    pems = []
    for store_name in ("CA", "ROOT"):
        with wincertstore.CertSystemStore(store_name) as store:
            for cert in store.itercerts(usage=wincertstore.SERVER_AUTH):
                try:
                    pem = cert.get_pem()
                    pem = pem.decode('ascii') if isinstance(
                        pem, bytes) else pem
                    pems.append(pem.strip())
                except:
                    pass

    return pems
