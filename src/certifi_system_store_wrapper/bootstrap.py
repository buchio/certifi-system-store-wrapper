# Copyright (c) 2025 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

from .logger import logger  # Import the logger for debug output
from .wrapper import wrap_functions  # Import the function to wrap certifi functions
import os
import site  # Used to patch site customization hooks
import wrapt  # Used for dynamic import hooks

_registered = False  # Flag to ensure bootstrap functions are registered only once


def _register_bootstrap_functions():
    """
    Register the wrapt hook for certifi if not already registered.
    This ensures that the certifi functions are wrapped only once.
    """
    logger.debug('Try to register wrap functions.')

    global _registered
    if _registered:
        logger.debug('Already registerd.')
        return
    _registered = True

    logger.debug('Register wrapt hook.')

    @wrapt.when_imported('certifi')
    def apply_certifi_patches(certifi):
        # Apply function wrapping to certifi when it is imported
        wrap_functions(certifi)


def _execsitecustomize_wrapper(wrapped):
    """
    Wrapper for site.execsitecustomize to trigger bootstrap after sitecustomize is loaded.

    This ensures that, if usercustomize is not enabled, the bootstrap functions
    are registered after sitecustomize is executed.
    """
    logger.debug('_execsitecustomize_wrapper')

    def _execsitecustomize(*args, **kwargs):
        logger.debug('_execsitecustomize')
        try:
            return wrapped(*args, **kwargs)
        finally:
            # Check whether 'usercustomize' support is actually disabled.
            # If so, register bootstrap functions after 'sitecustomize' is loaded.
            if not site.ENABLE_USER_SITE:
                _register_bootstrap_functions()
    return _execsitecustomize


def _execusercustomize_wrapper(wrapped):
    """
    Wrapper for site.execusercustomize to trigger bootstrap after usercustomize is loaded.

    This always registers the bootstrap functions after usercustomize is executed.
    """
    logger.debug('_execusercustomize_wrapper')

    def _execusercustomize(*args, **kwargs):
        logger.debug('_execusercustomize_wrapper')
        try:
            return wrapped(*args, **kwargs)
        finally:
            # Always register bootstrap functions after usercustomize is loaded.
            _register_bootstrap_functions()
    return _execusercustomize


def bootstrap() -> None:
    """
    Patch site.execsitecustomize and site.execusercustomize to ensure
    bootstrap functions are registered at the appropriate time during interpreter startup.

    This function replaces the original site customization hooks with wrappers
    that trigger the registration of certifi-system-store-wrapper's bootstrap logic.
    """
    site.execsitecustomize = _execsitecustomize_wrapper(site.execsitecustomize)
    site.execusercustomize = _execusercustomize_wrapper(site.execusercustomize)
