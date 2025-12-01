"""ルーティング設定."""

from flask import Flask
from views.login import login_bp
from views.top import top_bp
from views.users import users_bp


def init_blueprint(app: Flask):
    """Blueprintを登録する."""
    app.register_blueprint(login_bp)
    app.register_blueprint(top_bp)
    app.register_blueprint(users_bp)
