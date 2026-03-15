import asyncio
import os
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import asyncpg
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
from asyncpg import Connection
from asyncpg.exceptions import UndefinedTableError

PROJECT_PATH = Path(__file__).resolve().parents[1]
ALEMBIC_INI_PATH = PROJECT_PATH / "alembic.ini"


@dataclass(frozen=True, slots=True)
class PostgresSettings:
    user: str
    password: str
    host: str
    port: int

    @classmethod
    def from_env(cls) -> "PostgresSettings":
        return cls(
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "5444")),
        )

    def asyncpg_kwargs(self, database: str) -> dict[str, str | int]:
        return {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "database": database,
        }

    def sqlalchemy_url(self, database: str) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{database}"


def make_alembic_config(*, database_url: str | None = None, base_path: Path = PROJECT_PATH) -> Config:
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        pg_url=database_url,
        raiseerr=False,
        x=None,
    )
    config_path = Path(cmd_options.config)
    if not config_path.is_absolute():
        config_path = base_path / config_path

    config = Config(file_=str(config_path), ini_section=cmd_options.name, cmd_opts=cmd_options)

    script_location = Path(config.get_main_option("script_location"))
    if not script_location.is_absolute():
        config.set_main_option("script_location", str(base_path / script_location))

    if database_url is not None:
        config.set_main_option("sqlalchemy.url", database_url)

    return config


def alembic_config_from_url(database: str) -> Config:
    postgres_settings = PostgresSettings.from_env()
    return make_alembic_config(database_url=postgres_settings.sqlalchemy_url(database))


def get_revisions() -> list[Script]:
    revisions_dir = ScriptDirectory.from_config(make_alembic_config())
    return list(reversed(list(revisions_dir.walk_revisions(base="base", head="heads"))))


async def _connect(database: str) -> Connection:
    postgres_settings = PostgresSettings.from_env()
    return await asyncpg.connect(**postgres_settings.asyncpg_kwargs(database))


async def _create_database(database: str) -> None:
    conn = await _connect("postgres")
    try:
        await conn.execute(f'CREATE DATABASE "{database}"')
    finally:
        await conn.close()


async def _drop_database(database: str) -> None:
    conn = await _connect("postgres")
    try:
        await conn.execute(
            """
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = $1 AND pid <> pg_backend_pid()
            """,
            database,
        )
        await conn.execute(f'DROP DATABASE IF EXISTS "{database}"')
    finally:
        await conn.close()


async def _current_revision(database: str) -> str | None:
    conn = await _connect(database)
    try:
        try:
            return await conn.fetchval("SELECT version_num FROM alembic_version LIMIT 1")
        except UndefinedTableError:
            return None
    finally:
        await conn.close()


def create_database(database: str) -> None:
    asyncio.run(_create_database(database))


def drop_database(database: str) -> None:
    asyncio.run(_drop_database(database))


def current_revision(database: str) -> str | None:
    return asyncio.run(_current_revision(database))
