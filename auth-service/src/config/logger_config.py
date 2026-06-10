"""
Configure logger.
module: src/config/logger_config.py
"""

import logging
import sys
from typing import cast
from flask import Flask


def configure_logger(app: Flask) -> None:
    """Configure loggers."""
    set_logger_env(app)
    formatter = get_logger_formatter()
    remove_logger_handler(app)
    add_logger_handler(app, formatter)


def set_logger_env(app: Flask) -> None:
    """Determine environment and set logger level."""
    is_debug: bool = cast(str, app.config["FLASK_DEBUG"]).lower() in ("true", "1", "t")

    if is_debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)


def get_logger_formatter() -> logging.Formatter:
    """Get formatter for logger."""
    return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def remove_logger_handler(app: Flask) -> None:
    """Remove any existing handlers."""
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)


def add_logger_handler(app: Flask, formatter: logging.Formatter) -> None:
    """Add a new handler for console output."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
