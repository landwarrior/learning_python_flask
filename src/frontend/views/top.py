"""トップ画面のビュー."""

from flask import Blueprint, render_template, session
from utils import get_common_data


top_bp = Blueprint("top", __name__, url_prefix="/")


@top_bp.route("")
def home():
    """トップ画面を表示する."""
    common_data = get_common_data()
    # たぶんセッションクッキーがちゃんと設定されているか見るためのテスト用に書いた気がする
    session["login_user"] = "fuga"
    return render_template("index.jinja", **common_data)
