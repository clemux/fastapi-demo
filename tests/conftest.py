import aiomysql
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.config import get_settings, Settings
from app.lib.db import get_db_connection
from app.main import app as local_app


@pytest.fixture
def anyio_backend():
    return "asyncio"


async def create_tables(db: aiomysql.Connection):
    with open("sql/init.sql") as f:
        script = f.read()

    async with db.cursor() as cursor:
        await cursor.execute(script)
    await db.commit()


async def drop_tables(db: aiomysql.Connection):
    async with db.cursor() as cursor:
        await cursor.execute("DROP TABLE IF EXISTS activation_codes;")
        await cursor.execute("DROP TABLE IF EXISTS users;")
    await db.commit()


@pytest.mark.anyio
@pytest.fixture()
async def db(anyio_backend):
    """Necessary for fixtures that must commit to the database."""
    settings = get_settings()
    conn = await get_db_connection(settings)
    await create_tables(conn)

    yield conn

    await drop_tables(conn)
    conn.close()


@pytest.fixture()
def app(db):
    yield local_app


@pytest.fixture()
def override_settings_email_error(app):
    """Fixture for changing the email endpoint to /errors."""
    app.dependency_overrides[get_settings] = lambda: Settings(
        email_service_endpoint="/email/error"
    )
    yield
    del app.dependency_overrides[get_settings]


@pytest.fixture()
def override_settings_email_slow(app):
    """Fixture for changing the email endpoint to /slow."""
    app.dependency_overrides[get_settings] = lambda: Settings(
        email_service_endpoint="/email/slow",
        email_service_timeout_seconds=2,
    )
    yield
    del app.dependency_overrides[get_settings]


@pytest.fixture()
def client(app):
    with TestClient(local_app) as test_client:
        yield test_client


@pytest.fixture()
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.mark.anyio
@pytest.fixture()
async def user(db):
    async with db.cursor() as cursor:
        query = (
            "INSERT INTO users VALUES ('ba8a4d9c-7e87-4400-a420-48400e079469',"
            "'user@example.com',"
            "'$pbkdf2-sha256$29000$21vLuff.nxNCKAXAmJNyTg$eUcS9gVhk14MZ4ex/0/E95RyR1MbYxhczsm02Yz9rng'"
            ", FALSE);"
        )
        await cursor.execute(query)
        await db.commit()

    yield


@pytest.mark.anyio
@pytest.fixture()
async def user_activated(db: aiomysql.Connection):
    async with db.cursor() as cursor:
        query = (
            "INSERT INTO users VALUES ('ba8a4d9c-7e87-4400-a420-48400e079469',"
            "'user@example.com',"
            "'$pbkdf2-sha256$29000$21vLuff.nxNCKAXAmJNyTg$eUcS9gVhk14MZ4ex/0/E95RyR1MbYxhczsm02Yz9rng'"
            ", TRUE);"
        )
        await cursor.execute(query)

        query = (
            "INSERT INTO activation_codes VALUES"
            " ('585d1146-dac4-4e74-ac26-7870a06aac00', 'ba8a4d9c-7e87-4400-a420-48400e079469',"
            " '2812', '2023-11-14 00:01:00');"
        )
        await cursor.execute(query)
        await db.commit()

    yield


@pytest.mark.anyio
@pytest.fixture()
async def activation_code(db: aiomysql.Connection, user):
    async with db.cursor() as cursor:
        query = (
            "INSERT INTO activation_codes VALUES"
            " ('585d1146-dac4-4e74-ac26-7870a06aac00', 'ba8a4d9c-7e87-4400-a420-48400e079469',"
            " '2812', '2023-11-14 00:01:00');"
        )
        await cursor.execute(query)
        await db.commit()

    yield
