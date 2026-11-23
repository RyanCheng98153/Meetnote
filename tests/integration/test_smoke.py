import pytest


@pytest.mark.integration
def test_fixtures_dir_exists(fixtures_dir):
    assert fixtures_dir.is_dir()
