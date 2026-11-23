"""共用 pytest fixtures。"""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    """測試資料目錄 tests/fixtures/。"""
    return FIXTURES_DIR
