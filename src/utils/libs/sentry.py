# -*- coding: utf-8 -*-
from logging import getLevelName, ERROR
import warnings

from colorama import Fore
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from ..config import SentryConfig


def init_sentry(config: SentryConfig, level: str):
    if config.sentry_dsn is None:
        warnings.warn(Fore.YELLOW + "Sentry DSN 无效，将不会启用 Sentry 功能" + Fore.RESET, RuntimeWarning)

    sentry_config = {
        key[7:]: value
        for key, value in config.serialize().items()
        if key != "sentry_environment"
    }
    sentry_sdk.init(
        **sentry_config,
        environment=config.sentry_environment,
        default_integrations=False,
        integrations=[LoggingIntegration(
            level=getLevelName(level),
            event_level=ERROR
        )]
    )
