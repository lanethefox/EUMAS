"""Logging configuration for EUMAS."""

import sys
import json
from typing import Optional

from loguru import logger

from eumas.config import Config


def setup_logging(log_level: Optional[str] = None, test_sink=None) -> None:
    """Set up logging configuration.
    
    Args:
        log_level: Optional override for the log level. If not provided,
                  uses the level from Config.
        test_sink: Optional sink for testing. If provided, logs will also be
                  written to this sink with a simple format.
    """
    # Remove default handler
    logger.remove()
    
    # Get log level from config if not provided
    level = log_level or Config.LOG_LEVEL
    
    # Configure format based on environment
    if Config.LOG_FORMAT.lower() == "json":
        # JSON logging for production/structured logging
        def json_formatter(record):
            """Format log record as JSON."""
            return json.dumps({
                "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
                "level": record["level"].name,
                "name": record["name"],
                "message": record["message"],
                "extra": record["extra"],
            }) + "\n"
        
        logger.add(
            sys.stdout,
            format=json_formatter,
            level=level,
            serialize=False,
        )
    else:
        # Human-readable format for development
        logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=level,
            colorize=True,
        )
    
    # Add test sink if provided
    if test_sink is not None:
        logger.add(test_sink, format="{message}", level=level)
    
    # Log configuration message
    logger.info(
        "Logging configured",
        extra={
            "level": level,
            "format": Config.LOG_FORMAT,
            "environment": Config.ENVIRONMENT,
        },
    )
