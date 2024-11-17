import logging
import time
import traceback
import uuid

from flask import Flask, Response, g, jsonify, request

from config import get_config
from models import Database
from mylogger import UniqueKeyFormatter
from routes import init_blueprint

app = Flask(__name__)


def prepare_logging(app: Flask) -> None:
    app.logger.handlers = []
    app.logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = UniqueKeyFormatter()
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def prepare_db(app: Flask) -> None:
    if not hasattr(app, "db"):
        app.db = Database(app.config.get("SQLALCHEMY_DATABASE_URI", ""))
    app.db.Base.prepare(autoload_with=app.db.engine)
    app.db.mst_user = app.db.Base.classes.mst_user


app.config.from_object(get_config())
app.json.ensure_ascii = False
prepare_logging(app)
prepare_db(app)


@app.route("/status")
def home():
    return "200 OK"


@app.before_request
def before_request():
    g.start_time = time.time()
    # UUID4 を 16 進数にして、 7 文字分だけ使う
    g.unique_key = uuid.uuid4().hex[0:7]
    data = request.get_json(silent=True)
    header = str(request.headers).strip().replace("\r", "").replace("\n", ", ")
    app.logger.info(f"[URL] {request.method} {request.url} [DATA] {data} [HEADER] {header}")


@app.after_request
def after_request(response: Response):
    duration = time.time() - g.start_time
    app.logger.info(f"[RESPONSE] [STATUS] {response.status_code} [JSON] {response.json} [{duration: .5f} sec]")
    if "application/json" in response.content_type:
        response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.errorhandler(404)
def handle_404_error(e):
    app.logger.info(f"error response: {e}")
    return jsonify({"code": 404, "message": "Not Found"}), 404


@app.errorhandler(Exception)
def handle_exception_error(e):
    app.logger.error(traceback.format_exc())
    app.logger.info(f"Unhandled exception: {e}")
    return jsonify({"code": 500, "message": "Internal Server Error"}), 500


@app.errorhandler(500)
def handle_500_error(e):
    app.logger.info(f"error response: {e}")
    return jsonify({"code": 500, "message": "Internal Server Error"}), 500


@app.errorhandler(502)
def handle_502_error(e):
    app.logger.info(f"error response: {e}")
    return jsonify({"code": 502, "message": "Internal Server Error"}), 502


init_blueprint(app)

if __name__ == "__main__":
    app.run(debug=True)
