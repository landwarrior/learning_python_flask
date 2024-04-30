from flask import Blueprint, current_app, jsonify
from models import session_scope

api_bp = Blueprint("api", __name__)


@api_bp.route("/", methods=["GET"])
def hello_world():
    return jsonify({"status": "ok"})


@api_bp.route("/users", methods=["GET"])
def get_users():
    data = []
    with session_scope(current_app.db.engine) as session:
        for cols in session.query(current_app.db.mst_user):
            data.append(
                {
                    "user_id": cols.user_id,
                    "user_name": cols.user_name,
                    "user_name_kan": cols.user_name_kana,
                    "email": cols.email,
                    "gender": cols.gender,
                    "age": cols.age,
                    "birth_day": cols.birth_day.strftime("%Y%m%d") if cols.birth_day else None,
                    "blood_type": cols.blood_type,
                    "prefecture": cols.prefecture,
                    "curry": cols.curry,
                }
            )
    return jsonify(data)
