from uuid import uuid4

import pytest
from alembic.config import Config
from asyncpg.exceptions import PostgresError

from tests.utils import alembic_config_from_url, create_database, drop_database


@pytest.fixture
def migration_database() -> str:
    database = f"alembic_test_{uuid4().hex}"
    try:
        create_database(database)
    except (OSError, PostgresError) as exc:
        pytest.skip(f"Postgres is not available for migration tests: {exc}. Run `make db-up` first.")

    try:
        yield database
    finally:
        try:
            drop_database(database)
        except (OSError, PostgresError):
            pass


@pytest.fixture
def alembic_config(migration_database: str) -> Config:
    return alembic_config_from_url(migration_database)
