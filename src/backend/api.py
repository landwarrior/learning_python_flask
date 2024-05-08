import datetime

from flask import Blueprint, Response, current_app, jsonify, request
from models import mst_user

api_bp = Blueprint("api", __name__)


@api_bp.route("/", methods=["GET"])
def hello_world():
    return jsonify({"status": "ok"})


@api_bp.route("/users", methods=["GET"])
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

    for cols in mst_user.get_data(current_app.db.engine, current_app.db, offset, limit, condition):
        data["data"].append(
            {
                "user_id": cols.user_id,
                "user_name": cols.user_name,
                "user_name_kana": cols.user_name_kana,
                "email": cols.email,
                "gender": cols.gender,
                "age": cols.age,
                "birth_day": cols.birth_day.strftime("%Y%m%d") if cols.birth_day else None,
                "blood_type": cols.blood_type,
                "prefecture": cols.prefecture,
                "curry": cols.curry,
            }
        )
        data["total"] = cols.total
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
        if user_id:
            condition["user_id"] = user_id
        if user_name:
            condition["user_name"] = user_name
        if user_name_kana:
            condition["user_name_kana"] = user_name_kana
        if email:
            condition["email"] = email
        if gender:
            condition["gender"] = gender
        if age:
            condition["age"] = int(age)
        if birth_day:
            condition["birth_day"] = datetime.datetime.strptime(birth_day, "%Y%m%d").date()
        if birth_day_from:
            condition["birth_day_from"] = datetime.datetime.strptime(birth_day_from, "%Y%m%d").date()
        if birth_day_to:
            condition["birth_day_to"] = datetime.datetime.strptime(birth_day_to, "%Y%m%d").date()
        if blood_type:
            condition["blood_type"] = blood_type
        if prefecture:
            condition["prefecture"] = prefecture
        if curry:
            condition["curry"] = curry
    except Exception as e:
        current_app.logger.info(f"invalid parameter: {e}")
        raise e from e
    return condition if condition else None
