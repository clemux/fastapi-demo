"""FastAPI dependencies."""

from typing import Annotated
from passlib.hash import pbkdf2_sha256

import aiomysql
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from app.config import get_settings
from app.lib.db import get_db_connection
from app.lib.users import get_user
from app.schemas.user import UserSchema

security = HTTPBasic()


async def get_db(
    settings: Annotated[get_settings, Depends(get_settings)],
):
    """Dependency for retrieving a database connection."""
    conn = await get_db_connection(settings)
    try:
        yield conn
    finally:
        conn.close()


async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[aiomysql.Connection, Depends(get_db)],
) -> UserSchema:
    """Check username and password and return current user."""
    # TODO: is this susceptible to timing attacks?
    user = await get_user(db, credentials.username)
    if not (user and pbkdf2_sha256.verify(credentials.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user
