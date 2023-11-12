"""Middlewares for logging and request context."""

import logging.config
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.lib.logging import (
    RequestLoggingContext,
    set_logging_context,
    reset_logging_context,
)

logger = logging.getLogger()


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware that sets a request context as a context var."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex)
        token = set_logging_context(RequestLoggingContext(request_id=request_id))
        response = await call_next(request)
        reset_logging_context(token)
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs HTTP requests."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        logger.info(
            "Processed HTTP request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
            },
        )
        return response
