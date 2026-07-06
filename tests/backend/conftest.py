"""backend API テスト用フィクスチャ."""

import os
from datetime import date

import pytest


# pytest 実行時は TestConfig (mydb_test) を使う
os.environ.setdefault("POSITION", "test")

# WORKDIR が /var/app/flask/tests のとき、tests/backend/ が backend モジュールより先に
# 解決されるのを防ぐ。
# pytest.ini の testpaths で tests/backend/ を指定している場合は不要。
# sys.path.insert(0, "/var/app/flask/backend")

from models import MstUser

from backend import app as flask_app


def _default_user_kwargs(**kwargs):
    defaults = {
        "user_id": "abe_masami",
        "user_name": "阿部 まさみ",
        "user_name_kana": "あべ まさみ",
        "ignition_key": "",
        "email": "abe_masami@example.com",
        "gender": "女",
        "age": 58,
        "birth_day": date(1965, 6, 8),
        "blood_type": "AB型",
        "prefecture": "群馬県",
        "curry": "手前ルー・ルー攻め派",
    }
    defaults.update(kwargs)
    return defaults


def insert_mst_user(db, **kwargs):
    """mst_user に 1 件挿入する."""
    with db.session_scope() as session:
        session.add(MstUser(**_default_user_kwargs(**kwargs)))


def insert_mst_users(db, users):
    """mst_user に複数件挿入する."""
    with db.session_scope() as session:
        for user in users:
            session.add(MstUser(**_default_user_kwargs(**user)))


def delete_all_mst_users(db):
    """mst_user の全レコードを削除する."""
    with db.session_scope() as session:
        session.query(MstUser).delete()


@pytest.fixture
def app():
    """テスト用 Flask アプリケーション."""
    yield flask_app


@pytest.fixture
def db(app):
    """テスト用 Database インスタンス."""
    return app.db


@pytest.fixture(autouse=True)
def clean_mst_user_table(db):
    """各テスト前後で mst_user を空にする (setUp / tearDown 相当)."""
    delete_all_mst_users(db)
    yield
    delete_all_mst_users(db)


@pytest.fixture
def client(app):
    """テストクライアント."""
    return app.test_client()
