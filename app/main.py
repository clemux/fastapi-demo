"""FastAPI application to demonstrate how to handle user registation"""

from fastapi import FastAPI

from app.routers import users

app = FastAPI()

app.include_router(users.router)
