from flask import Blueprint, render_template, session
from utils import get_common_data

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/list")
def home():
    common_data = get_common_data()
    session["hoge"] = "fuga"
    return render_template("users/list.jinja", **common_data)
