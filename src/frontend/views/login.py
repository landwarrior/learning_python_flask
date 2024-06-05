import requests
from flask import Blueprint, current_app, redirect, render_template, request, session, url_for

login_bp = Blueprint("login", __name__, url_prefix="/login")


@login_bp.route("", methods=["GET"])
def login_form():
    return render_template("login.jinja")


@login_bp.route("", methods=["POST"])
def login():
    request_data = {"login_id": request.form.get("login_id"), "ignition_key": request.form.get("ignition_key")}
    current_app.logger.info(f"ACCESS: {current_app.config['BACKEND_URL'] + '/login'} DATA: {request_data}")
    data = requests.post(current_app.config["BACKEND_URL"] + "/login", json=request_data)
    current_app.logger.info(f"RESPONSE: {data}")
    if data.status_code == 200:
        session["login_user"] = data.json()["user_id"]
        return redirect(url_for("top"))
    else:
        return render_template("login.jinja", error="ユーザーIDまたはパスワードが間違っています。")
