from flask import Blueprint, redirect, render_template, request, session, url_for
from utils import validate_user_credentials

login_bp = Blueprint("login", __name__, url_prefix="/login")


@login_bp.route("", methods=["GET"])
def login_form():
    return render_template("login.jinja")


@login_bp.route("", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if validate_user_credentials(username, password):
        session["user"] = username
        return redirect(url_for("home"))
    else:
        return render_template("login.jinja", error="ユーザー名またはパスワードが間違っています。")
