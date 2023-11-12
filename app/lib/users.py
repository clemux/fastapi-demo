"""Database operations for users."""
from datetime import datetime

import aiomysql

from app.exceptions import EmailAlreadyExistsException
from app.schemas.user import UserSchema


async def insert_user(conn: aiomysql.Connection, user: UserSchema):
    """Inserts a user into the database."""
    async with conn.cursor() as cursor:
        query_check_email = f"SELECT email FROM users WHERE email = '{user.email}'"
        result = await cursor.execute(query_check_email)
        if result:
            raise EmailAlreadyExistsException()
        query_insert = (
            f"INSERT INTO users (id, email, password, activated) "
            f"VALUES ('{user.id}', '{user.email}', '{user.password}', {user.activated})"
        )
        await cursor.execute(query_insert)


async def activate_user(conn: aiomysql.Connection, user: UserSchema, code: int):
    """Activate a user in the database."""
    async with conn.cursor() as cursor:
        query = (
            f"SELECT code, expiration FROM activation_codes WHERE user_id = '{user.id}' "
            "ORDER BY expiration DESC LIMIT 1"
        )
        await cursor.execute(query)
        result = await cursor.fetchone()
        if not result:
            return False
        expected_code, expiration = result
        if expected_code == code and expiration > datetime.now():
            return True
        return False


async def get_user(conn: aiomysql.Connection, email: str):
    """Retrieve a user from the database."""
    query = f"SELECT id, email, activated, password FROM users where email = '{email}';"
    async with conn.cursor() as cursor:
        await cursor.execute(query=query)
        result = await cursor.fetchone()
        if result:
            user_id, email, activated, password = result
            return UserSchema(
                id=user_id, email=email, activated=activated, password=password
            )
    return None
