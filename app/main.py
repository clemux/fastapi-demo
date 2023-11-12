"""FastAPI application to demonstrate how to handle user registration"""
from fastapi import FastAPI

from app.lib.logging import setup_logging
from app.middlewares import LoggingMiddleware, RequestContextMiddleware
from app.routers import healthcheck, users

setup_logging()

app = FastAPI()

app.include_router(users.router)
app.include_router(healthcheck.router)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestContextMiddleware)
