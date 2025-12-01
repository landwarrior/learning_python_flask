"""ログイン画面のビュー."""

import requests
from flask import (
    Blueprint,
    current_app,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


login_bp = Blueprint("login", __name__, url_prefix="/login")


@login_bp.route("", methods=["GET"])
def login_form():
    """ログイン画面を表示する."""
    # ログイン処理時の flash メッセージを取得
    error = get_flashed_messages(category_filter=["error"])
    if isinstance(error, list) and len(error) > 0:
        error = error[0]  # type: ignore
    return render_template("login.jinja", error=error)


@login_bp.route("", methods=["POST"])
def login():
    """ログイン処理を行う."""
    request_data = {"login_id": request.form.get("login_id"), "ignition_key": request.form.get("ignition_key")}
    current_app.logger.info(f"ACCESS: {current_app.config['BACKEND_URL'] + '/login'} DATA: {request_data}")
    data = requests.post(current_app.config["BACKEND_URL"] + "/login", json=request_data)
    current_app.logger.info(f"RESPONSE: {data.status_code} {data.json()}")
    if data.status_code == 200:
        session["login_user"] = data.json()["user_id"]
        return redirect(url_for("top.home"))
    else:
        flash("ログインIDまたはパスワードが間違っています。", "error")
        return redirect(url_for("login.login_form"))
