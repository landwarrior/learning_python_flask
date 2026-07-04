"""backend API テスト用フィクスチャ."""

import sys
from pathlib import Path

import pytest


def _prepend_sys_path(path: Path) -> None:
    entry = str(path)
    if path.is_dir() and entry not in sys.path:
        sys.path.insert(0, entry)


# WORKDIR が /var/app/flask/tests のとき、tests/backend/ が backend モジュールより先に
# 解決されるのを防ぐ。
_prepend_sys_path(Path("/var/app/flask/backend"))

from backend import app as flask_app


@pytest.fixture
def app():
    """テスト用 Flask アプリケーション."""
    flask_app.config.update({"TESTING": True})
    yield flask_app


@pytest.fixture
def client(app):
    """テストクライアント."""
    return app.test_client()
