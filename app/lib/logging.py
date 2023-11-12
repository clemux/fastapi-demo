"""Logging context management."""
import logging
import logging.config
from contextvars import ContextVar

from pythonjsonlogger import jsonlogger
from pydantic import BaseModel


class RequestLoggingContext(BaseModel):
    """Request context for logging."""

    request_id: str | None


_logging_context_var = ContextVar[RequestLoggingContext](
    "logging_context", default=None
)


def get_logging_context():
    return _logging_context_var.get()


def set_logging_context(logging_context: RequestLoggingContext):
    return _logging_context_var.set(logging_context)


def reset_logging_context(token):
    _logging_context_var.reset(token)


class ContextFilter(logging.Filter):
    """
    Filter which injects the request id into the log record.
    """

    def filter(self, record):
        logging_context = get_logging_context()
        if logging_context:
            record.request_id = get_logging_context().request_id
        return True


def setup_logging():
    """Setup logging with json formatter and context filter."""
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": jsonlogger.JsonFormatter,
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                }
            },
            "filters": {"context_filter": {"()": ContextFilter}},
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "filters": ["context_filter"],
                }
            },
            "root": {"handlers": ["console"], "level": "INFO"},
        }
    )
