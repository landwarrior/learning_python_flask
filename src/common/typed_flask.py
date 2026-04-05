"""Flask アプリと current_app 用の型付きヘルパー."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from flask import Flask, current_app


if TYPE_CHECKING:
    from models import Database


class FlaskApp(Flask):
    """Database を app.db として保持するアプリケーション(型チェック用)."""

    db: Database


def get_db() -> Database:
    """current_app から Database を取得する(Pyright / mypy 向け)."""
    return cast("FlaskApp", current_app).db
