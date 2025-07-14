# Copyright (c) 2025 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

import logging
import os

# Create a logger for the certifi_system_store_wrapper package
logger = logging.getLogger('certifi_system_store_wrapper')

# Set the log message format
_f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the logger level from environment variable, default to WARNING
logger.setLevel(os.environ.get('PYTHON_CERTIFI_LOG_LEVEL', 'WARNING'))

# Create a stream handler for console output
_h = logging.StreamHandler()
_h.setLevel(os.environ.get('PYTHON_CERTIFI_LOG_LEVEL', 'WARNING'))
_h.setFormatter(_f)
logger.addHandler(_h)

# If a log file is specified in the environment, add a file handler
_log_filename = os.environ.get('PYTHON_CERTIFI_LOG_FILE')
if _log_filename is not None:
    _h = logging.FileHandler(_log_filename)
    _h.setFormatter(_f)
    _h.setLevel(os.environ.get('PYTHON_CERTIFI_LOG_FILE_LEVEL', 'DEBUG'))
    logger.addHandler(_h)
