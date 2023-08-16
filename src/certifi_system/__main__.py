# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

import certifi
import certifi_system


def main() -> None:
    print(f'certifi-system version [{certifi_system.version}]')
    print(f'certifi-system where [{certifi.where()}]')
    print(f'certifi-system contents [{len(certifi.contents())}]')


if __name__ == "__main__":
    main()
