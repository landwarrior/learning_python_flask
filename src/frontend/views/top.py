from flask import Blueprint, render_template, session

top_bp = Blueprint("top", __name__, url_prefix="/")


@top_bp.route("")
def home():
    session["hoge"] = "fuga"
    return render_template("index.jinja")
