"""ユーザ画面のビュー."""

import time

import requests
from flask import Blueprint, Response, current_app, jsonify, render_template, request
from utils import get_common_data


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/list")
def home():
    """ユーザ画面を表示する."""
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


@users_bp.route("/api/modal/showable/<user_id>", methods=["POST"])
def api_list_user_id(user_id: str) -> Response:
    """モーダル画面に表示するための情報を返す.

    面倒なのでハードコードする.
    user_id を指定しているけど、まだ使う予定はない.

    Args:
        user_id (str): ログインユーザID

    Returns:
        Response: Flask の Response オブジェクト
    """
    current_app.logger.info(f"user_id: {user_id}")
    # 検索時に target に対応するデータを埋め込んでいて、それを label ごとにモーダル画面で読み込んでるだけ
    settings = [
        {"target": "user_id", "label": "社員ID"},
        {"target": "user_name", "label": "社員名"},
        {"target": "user_name_kana", "label": "社員名かな"},
        {"target": "email", "label": "email"},
        {"target": "gender", "label": "性別"},
        {"target": "age", "label": "年齢"},
        {"target": "birth_day", "label": "生年月日"},
        {"target": "blood_type", "label": "血液型"},
        {"target": "prefecture", "label": "都道府県"},
        {"target": "curry", "label": "カレーの食べ方"},
    ]
    return jsonify(settings)
