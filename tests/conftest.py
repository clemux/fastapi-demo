from typing import Annotated

import aiomysql
import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.config import get_settings
from app.dependencies import get_db
from app.lib.db import get_db_connection
from app.main import app as local_app


async def get_test_db(
    settings: Annotated[get_settings, Depends(get_settings)],
):
    conn: aiomysql.Connection = await aiomysql.connect(
        host=settings.database_host,
        port=settings.database_port,
        user=settings.database_user,
        password=settings.database_password,
        db=settings.database_name,
        autocommit=False,
    )
    try:
        yield conn
    finally:
        await conn.rollback()
        conn.close()


@pytest.fixture()
def app():
    local_app.dependency_overrides[get_db] = get_test_db
    yield local_app


@pytest.fixture()
def client(app):
    with TestClient(local_app) as test_client:
        yield test_client


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture()
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.mark.anyio
@pytest.fixture()
async def db(anyio_backend):
    settings = get_settings()
    conn = await get_db_connection(settings)
    yield conn
    conn.close()


@pytest.mark.anyio
@pytest.fixture()
async def user(db: aiomysql.Connection):
    async with db.cursor() as cursor:
        query = (
            "INSERT INTO users VALUES ('ba8a4d9c-7e87-4400-a420-48400e079469',"
            "'user@example.com',"
            "'\$pbkdf2-sha256$29000$21vLuff.nxNCKAXAmJNyTg$eUcS9gVhk14MZ4ex/0/E95RyR1MbYxhczsm02Yz9rng'"
            ", FALSE);"
        )
        await cursor.execute(query)
        await db.commit()

    yield

    query_delete = "DELETE FROM users WHERE email = 'user@example.com';"
    async with db.cursor() as cursor:
        await cursor.execute(query_delete)
        await db.commit()


@pytest.mark.anyio
@pytest.fixture()
async def activation_code(db: aiomysql.Connection, user):
    async with db.cursor() as cursor:
        query = (
            "INSERT INTO activation_codes VALUES"
            " ('585d1146-dac4-4e74-ac26-7870a06aac00', 'ba8a4d9c-7e87-4400-a420-48400e079469',"
            " 2812, '2023-11-14 00:01:00');"
        )
        await cursor.execute(query)
        await db.commit()

    yield

    query_delete_activation_code = "DELETE FROM activation_codes WHERE code = '2812';"
    async with db.cursor() as cursor:
        await cursor.execute(query_delete_activation_code)
        await db.commit()
