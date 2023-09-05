# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .logger import logger
from .wrapper import wrap_functions
import os
import site
import wrapt

_registered = False


def _register_bootstrap_functions():
    logger.debug('Try to register wrap functions.')

    global _registered
    if _registered:
        logger.debug('Already registerd.')
        return
    _registered = True

    logger.debug('Register wrapt hook.')

    @wrapt.when_imported('certifi')
    def apply_certifi_patches(certifi):
        wrap_functions(certifi)


def _execsitecustomize_wrapper(wrapped):
    logger.debug('_execsitecustomize_wrapper')

    def _execsitecustomize(*args, **kwargs):
        logger.debug('_execsitecustomize')
        try:
            return wrapped(*args, **kwargs)
        finally:
            # Check whether 'usercustomize' support is actually disabled.
            # In that case we do our work after 'sitecustomize' is loaded.

            if not site.ENABLE_USER_SITE:
                _register_bootstrap_functions()
    return _execsitecustomize


def _execusercustomize_wrapper(wrapped):
    logger.debug('_execusercustomize_wrapper')

    def _execusercustomize(*args, **kwargs):
        logger.debug('_execusercustomize_wrapper')
        try:
            return wrapped(*args, **kwargs)
        finally:
            _register_bootstrap_functions()
    return _execusercustomize


def bootstrap() -> None:
    site.execsitecustomize = _execsitecustomize_wrapper(site.execsitecustomize)
    site.execusercustomize = _execusercustomize_wrapper(site.execusercustomize)
