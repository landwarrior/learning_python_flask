import requests
from flask import Blueprint, current_app, jsonify, render_template, request, session
from utils import get_common_data

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/list")
def home():
    common_data = get_common_data()
    session["hoge"] = "fuga"
    return render_template("users/list.jinja", **common_data)


@users_bp.route("/api/list", methods=["POST"])
def api_list():
    json_data = request.get_json(silent=True)
    current_app.logger.info(json_data)
    data = requests.get(current_app.config.BACKEND_URL + "/users")

    return jsonify(data)
