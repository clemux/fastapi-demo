"""Database connection handling functions"""

import aiomysql

from app.config import Settings


async def get_db_connection(settings: Settings):
    """Get a database connection."""
    conn: aiomysql.Connection = await aiomysql.connect(
        host=settings.database_host,
        port=settings.database_port,
        user=settings.database_user,
        password=settings.database_password,
        db=settings.database_name,
    )
    return conn
