"""backend API テスト用フィクスチャ."""

import sys

import pytest


# WORKDIR が /var/app/flask/tests のとき、tests/backend/ が backend モジュールより先に
# 解決されるのを防ぐ。
sys.path.insert(0, "/var/app/flask/backend")

from backend import app as flask_app


@pytest.fixture
def app():
    """テスト用 Flask アプリケーション."""
    yield flask_app


@pytest.fixture
def client(app):
    """テストクライアント."""
    return app.test_client()
