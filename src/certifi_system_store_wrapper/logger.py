# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

import logging
import os

logger = logging.getLogger('certifi_system_store_wrapper')

_f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger.setLevel(os.environ.get('PYTHON_CERTIFI_LOG_LEVEL', 'WARNING'))
_h = logging.StreamHandler()
_h.setLevel(os.environ.get('PYTHON_CERTIFI_LOG_LEVEL', 'WARNING'))
_h.setFormatter(_f)
logger.addHandler(_h)

_log_filename = os.environ.get('PYTHON_CERTIFI_LOG_FILE')
if _log_filename is not None:
    _h = logging.FileHandler(_log_filename)
    _h.setFormatter(_f)
    _h.setLevel(os.environ.get('PYTHON_CERTIFI_LOG_FILE_LEVEL', 'DEBUG'))
    logger.addHandler(_h)
