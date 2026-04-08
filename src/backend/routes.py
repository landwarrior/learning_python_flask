"""ルーティング設定."""

from typing import TYPE_CHECKING

from csv_api import csv_bp
from v1.login import login_bp
from v1.users import users_bp


if TYPE_CHECKING:
    from flask import Flask


def init_blueprint(app: Flask):
    """Blueprintを登録する."""
    app.register_blueprint(login_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(csv_bp)
