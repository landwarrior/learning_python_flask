from flask import Blueprint, jsonify
from models import mst_user

api_bp = Blueprint("api", __name__)


@api_bp.route("/", methods=["GET"])
def hello_world():
    return jsonify({"status": "ok"})


@api_bp.route("/users", methods=["GET"])
def get_users():
    users = mst_user.query.all()
    return jsonify(users)
