"""ログイン処理API."""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import Blueprint, Response, current_app, jsonify, request
from models import mst_user


login_bp = Blueprint("login", __name__)

# Argon2 のパスワードハッシャーを初期化
ph = PasswordHasher(
    time_cost=2,  # 反復回数: パスワードハッシュ化の計算コストを制御。値が大きいほど強力だが処理時間も増える
    memory_cost=65536,  # メモリ使用量(KB): 65536KB = 64MB。メモリハードな計算によりGPU攻撃を防ぐ
    parallelism=2,  # 並列度: 並列処理に使用するスレッド数。メモリ使用量に影響する
)


@login_bp.route("/login", methods=["POST"])
def login() -> tuple[Response, int]:
    """ログイン処理.

    Returns:
        tuple[Response, int]: レスポンスデータとステータスコード.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request"}), 400
    login_id = data.get("login_id", None)
    ignition_key = data.get("ignition_key", None)

    if not login_id or not ignition_key:
        return jsonify({"message": "Invalid username or password"}), 400

    user = mst_user.get_user_by_user_id(current_app.logger, current_app.db, login_id)
    if not user:
        return jsonify({"message": "password not match"}), 400

    try:
        ph.verify(user.ignition_key, ignition_key)
    except VerifyMismatchError:
        return jsonify({"message": "password not match"}), 400
    except Exception:
        return jsonify({"message": "password not match"}), 400

    return jsonify({"message": "Login successful", "user_id": user.user_id}), 200


@login_bp.route("/change_password", methods=["POST"])
def change_password() -> tuple[Response, int]:
    """パスワード変更処理.

    Returns:
        tuple[Response, int]: レスポンスデータとステータスコード.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request"}), 400
    user_id = data.get("user_id", None)
    old_password = data.get("old_password", None)
    new_password = data.get("new_password", None)

    if not user_id or not old_password or not new_password:
        return jsonify({"message": "Invalid username or password"}), 400

    user = mst_user.get_user_by_user_id(current_app.logger, current_app.db, user_id)

    if not user:
        return jsonify({"message": "Invalid username or password"}), 400

    try:
        ph.verify(user.ignition_key, old_password)
    except VerifyMismatchError:
        return jsonify({"message": "Invalid username or password"}), 400
    except Exception:
        return jsonify({"message": "Invalid username or password"}), 400

    user.ignition_key = ph.hash(new_password)
    current_app.db.session.commit()

    return jsonify({"message": "Password changed successfully"}), 200


@login_bp.route("/initialize_password", methods=["POST"])
def initialize_password() -> tuple[Response, int]:
    """パスワードを初期化する.

    初期パスワードは password とする.

    Returns:
        tuple[Response, int]: レスポンスデータとステータスコード.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid request"}), 400
    user_id = data.get("user_id", None)

    if not user_id:
        return jsonify({"message": "Invalid username"}), 400

    user = mst_user.get_user_by_user_id(current_app.logger, current_app.db, user_id)

    if not user:
        return jsonify({"message": "Invalid username"}), 400

    user.ignition_key = ph.hash("password")
    current_app.db.session.commit()

    return jsonify({"message": "Password initialized successfully"}), 200
