"""
Error Handler Module for Telegram Bot
Provides global exception handling and logging for all event handlers
"""

import logging
import functools
from typing import Callable, Any
from telethon import events

# Configure logging
import sys

# Create file handler
file_handler = logging.FileHandler('bot_errors.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Create console handler with UTF-8 encoding (fixes Windows emoji issue)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
# Force UTF-8 encoding on console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

logger = logging.getLogger(__name__)


def safe_event_handler(func: Callable) -> Callable:
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {type(e).__name__}: {e}", exc_info=True)
            try:
                event = args[0] if args else None
                if event and hasattr(event, 'respond'):
                    await event.respond(
                        "⚠️ An error occurred while processing your request. "
                        "The bot is still running and you can try again."
                    )
            except Exception:
                pass  
    return wrapper


def safe_function(func: Callable) -> Callable:
    """
    Decorator for non-event functions to add error logging without raising.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {type(e).__name__}: {e}", exc_info=True)
            raise  # Re-raise but after logging
    return wrapper


def log_info(message: str):
    """Log info message"""
    logger.info(message)


def log_error(message: str, exc_info: bool = False):
    """Log error message"""
    logger.error(message, exc_info=exc_info)


def log_warning(message: str):
    """Log warning message"""
    logger.warning(message)
