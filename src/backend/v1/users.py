import datetime

from flask import Blueprint, Response, current_app, jsonify, request
from models import mst_user

users_bp = Blueprint("users", __name__)


@users_bp.route("/", methods=["GET"])
def hello_world():
    return jsonify({"status": "ok"})


@users_bp.route("/users", methods=["GET"])
def get_users() -> Response:
    """ユーザーデータの取得.

    Returns:
        Response: レスポンスデータ.
    """
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=1000, type=int)
    try:
        condition = _param_to_condition()
    except Exception as e:
        return jsonify({"code": 400, "message": str(e)}), 400
    data = {
        "code": 200,
        "total": 0,
        "offset": offset,
        "limit": limit,
        "data": [],
    }

    for user in mst_user.get_data(current_app.db.engine, current_app.db, offset, limit, condition):
        data["data"].append(
            {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "user_name_kana": user.user_name_kana,
                "email": user.email,
                "gender": user.gender,
                "age": user.age,
                "birth_day": user.birth_day.strftime("%Y%m%d") if user.birth_day else None,
                "blood_type": user.blood_type,
                "prefecture": user.prefecture,
                "curry": user.curry,
            }
        )
        data["total"] = user.total
    return jsonify(data)


def _param_to_condition():
    user_id = request.args.get("user_id", default="", type=str)
    user_name = request.args.get("user_name", default="", type=str)
    user_name_kana = request.args.get("user_name_kana", default="", type=str)
    email = request.args.get("email", default="", type=str)
    gender = request.args.get("gender", default="", type=str)
    age = request.args.get("age", default="", type=str)
    birth_day = request.args.get("birth_day", default="", type=str)
    birth_day_from = request.args.get("birth_day_from", default="", type=str)
    birth_day_to = request.args.get("birth_day_to", default="", type=str)
    blood_type = request.args.get("blood_type", default="", type=str)
    prefecture = request.args.get("prefecture", default="", type=str)
    curry = request.args.get("curry", default="", type=str)
    condition = {}
    try:
        params = {
            "user_id": user_id,
            "user_name": user_name,
            "user_name_kana": user_name_kana,
            "email": email,
            "gender": gender,
            "age": int(age) if age else None,
            "birth_day": datetime.datetime.strptime(birth_day, "%Y%m%d").date() if birth_day else None,
            "birth_day_from": datetime.datetime.strptime(birth_day_from, "%Y%m%d").date() if birth_day_from else None,
            "birth_day_to": datetime.datetime.strptime(birth_day_to, "%Y%m%d").date() if birth_day_to else None,
            "blood_type": blood_type,
            "prefecture": prefecture,
            "curry": curry,
        }
        condition = {k: v for k, v in params.items() if v}
    except Exception as e:
        current_app.logger.info(f"invalid parameter: {e}")
        raise e from e
    return condition if condition else None
