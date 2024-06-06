import bcrypt
from flask import Blueprint, current_app, jsonify, request
from models import mst_user

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def login():
    """ログイン処理."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request"}), 400
    login_id = data.get("login_id", None)
    ignition_key = data.get("ignition_key", None)

    if not login_id or not ignition_key:
        return jsonify({"message": "Invalid username or password"}), 400

    user = mst_user.get_user_by_user_id(current_app.logger, current_app.db.engine, current_app.db, login_id)
    if not user or not bcrypt.checkpw(ignition_key.encode("utf-8"), user.ignition_key.encode("utf-8")):
        return jsonify({"message": "password not match"}), 400

    return jsonify({"message": "Login successful", "user_id": user.user_id})


@login_bp.route("/change_password", methods=["POST"])
def change_password():
    """パスワード変更処理."""
    user_id = request.json.get("user_id", None)
    old_password = request.json.get("old_password", None)
    new_password = request.json.get("new_password", None)

    if not user_id or not old_password or not new_password:
        return jsonify({"message": "Invalid username or password"}), 400

    user = mst_user.get_user_by_user_id(current_app.db.engine, current_app.db, user_id)

    if not user or not bcrypt.checkpw(old_password, user.ignition_key):
        return jsonify({"message": "Invalid username or password"}), 400

    user.ignition_key = bcrypt.hashpw(new_password, bcrypt.gensalt())
    current_app.db.session.commit()

    return jsonify({"message": "Password changed successfully"})


@login_bp.route("/initialize_password", methods=["POST"])
def initialize_password():
    """パスワードを初期化する.

    初期パスワードは password とする.
    """
    user_id = request.json.get("user_id", None)

    if not user_id:
        return jsonify({"message": "Invalid username"}), 400

    user = mst_user.get_user_by_user_id(current_app.db.engine, current_app.db, user_id, current_app.logger)

    if not user:
        return jsonify({"message": "Invalid username"}), 400

    user.ignition_key = bcrypt.hashpw("password", bcrypt.gensalt())
    current_app.db.session.commit()

    return jsonify({"message": "Password initialized successfully"})
