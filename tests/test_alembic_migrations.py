import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script

from tests.utils import current_revision, get_revisions


@pytest.mark.migration
def test_alembic_revisions_exist() -> None:
    assert get_revisions(), "No Alembic revisions found."


@pytest.mark.migration
@pytest.mark.parametrize("revision", get_revisions(), ids=lambda revision: revision.revision)
def test_migrations_stairway(alembic_config: Config, migration_database: str, revision: Script) -> None:
    if isinstance(revision.down_revision, tuple):
        pytest.skip("Branched migration graphs are not supported by the template stairway test.")

    upgrade(alembic_config, revision.revision)
    assert current_revision(migration_database) == revision.revision

    downgrade_target = revision.down_revision or "base"
    downgrade(alembic_config, downgrade_target)
    expected_revision = None if downgrade_target == "base" else downgrade_target
    assert current_revision(migration_database) == expected_revision

    upgrade(alembic_config, revision.revision)
    assert current_revision(migration_database) == revision.revision
