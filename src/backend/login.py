import bcrypt
from flask import Blueprint, current_app, jsonify, request
from models import mst_user

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def login():
    """ログイン処理."""
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"message": "Invalid username or password"}), 400

    user = mst_user.get_user_by_username(current_app.db.engine, current_app.db, username)

    if not user or not bcrypt.checkpw(password, user.password):
        return jsonify({"message": "Invalid username or password"}), 400

    return jsonify({"message": "Login successful"}), 200


@login_bp.route("/change_password", methods=["POST"])
def change_password():
    """パスワード変更処理."""
    username = request.json.get("username", None)
    old_password = request.json.get("old_password", None)
    new_password = request.json.get("new_password", None)

    if not username or not old_password or not new_password:
        return jsonify({"message": "Invalid username or password"}), 400

    user = mst_user.get_user_by_username(current_app.db.engine, current_app.db, username)

    if not user or not bcrypt.checkpw(old_password, user.password):
        return jsonify({"message": "Invalid username or password"}), 400

    user.password = bcrypt.hashpw(new_password, bcrypt.gensalt())
    current_app.db.session.commit()

    return jsonify({"message": "Password changed successfully"}), 200


@login_bp.route("/initialize_password", methods=["POST"])
def initialize_password():
    """パスワードを初期化する.

    初期パスワードは password とする.
    """
    username = request.json.get("username", None)

    if not username:
        return jsonify({"message": "Invalid username"}), 400

    user = mst_user.get_user_by_username(current_app.db.engine, current_app.db, username)

    if not user:
        return jsonify({"message": "Invalid username"}), 400

    user.password = bcrypt.hashpw("password", bcrypt.gensalt())
    current_app.db.session.commit()

    return jsonify({"message": "Password initialized successfully"}), 200
