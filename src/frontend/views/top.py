from flask import Blueprint, render_template, session
from utils import get_common_data

top_bp = Blueprint("top", __name__, url_prefix="/")


@top_bp.route("")
def home():
    common_data = get_common_data()
    session["hoge"] = "fuga"
    return render_template("index.jinja", **common_data)
