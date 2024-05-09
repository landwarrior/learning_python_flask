import time

import requests
from flask import Blueprint, Response, current_app, jsonify, render_template, request
from utils import get_common_data

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/list")
def home():
    common_data = get_common_data()
    return render_template("users/list.jinja", **common_data)


@users_bp.route("/api/list", methods=["POST"])
def api_list() -> Response:
    """ユーザの一覧を json 形式で返す.

    Returns:
        Response: Flask の Response オブジェクト
    """
    json_data = request.get_json(silent=True)
    # 早すぎて動作確認できないので sleep を入れる
    time.sleep(0.5)
    data = requests.get(current_app.config["BACKEND_URL"] + "/users", params=json_data).json()

    return jsonify(data)
