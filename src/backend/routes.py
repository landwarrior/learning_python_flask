from csv_api import csv_bp
from flask import Flask

from v1.login import login_bp
from v1.users import users_bp


def init_blueprint(app: Flask):
    app.register_blueprint(login_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(csv_bp)
