from flask import Blueprint, render_template, session

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/list")
def home():
    session["hoge"] = "fuga"
    return render_template("users/list.jinja")
