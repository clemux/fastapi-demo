"""Database operations for users."""
import uuid
from datetime import datetime, timedelta

import aiomysql

from app.exceptions import (
    EmailAlreadyExistsException,
    UserNotFoundException,
    InvalidActivationCodeException,
)
from app.schemas.user import UserSchema


async def insert_user(cursor: aiomysql.Cursor, user: UserSchema):
    """Inserts a user into the database."""
    query_check_email = "SELECT email FROM users WHERE email = %s"
    result = await cursor.execute(query_check_email, (user.email,))
    if result:
        raise EmailAlreadyExistsException()
    query_insert = (
        "INSERT INTO users (id, email, password, activated) " "VALUES (%s, %s, %s, %s)"
    )
    await cursor.execute(query_insert, (user.id, user.email, user.password, False))


async def insert_activation_code(
    cursor: aiomysql.Cursor,
    user: UserSchema,
    code: str,
    expiration_seconds: int,
):
    """Inserts an activation code into the database."""
    query = (
        "INSERT INTO activation_codes (id, user_id, code, expiration) "
        "VALUES (%s, %s, %s, %s)"
    )
    await cursor.execute(
        query,
        (
            uuid.uuid4(),
            user.id,
            code,
            datetime.now() + timedelta(seconds=expiration_seconds),
        ),
    )


async def activate_user(cursor: aiomysql.Cursor, user: UserSchema, code: str):
    """Activate a user in the database."""
    query = (
        "SELECT code, expiration FROM activation_codes WHERE user_id = %s "
        "ORDER BY expiration DESC LIMIT 1"
    )
    await cursor.execute(query, (user.id,))
    result = await cursor.fetchone()
    if not result:
        raise UserNotFoundException()
    expected_code, expiration = result
    if expected_code == code and expiration > datetime.now():
        activate_query = "UPDATE users SET activated = TRUE WHERE id = %s"
        await cursor.execute(activate_query, (user.id,))
        return True
    raise InvalidActivationCodeException()


async def get_user(conn: aiomysql.Connection, email: str):
    """Retrieve a user from the database."""
    query = "SELECT id, email, activated, password FROM users where email = %s"
    async with conn.cursor() as cursor:
        await cursor.execute(query, (email,))
        result = await cursor.fetchone()
        if result:
            user_id, email, activated, password = result
            return UserSchema(
                id=user_id, email=email, activated=activated, password=password
            )
    return None
