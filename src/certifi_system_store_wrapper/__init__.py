# Copyright (c) 2025 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

"""
The certifi_system_store_wrapper package.

This package provides functionality to integrate and manage the certificate store
using the certifi-system package. It includes version information and a bootstrap
function for initialization.
"""

from ._version import version
from .bootstrap import bootstrap
