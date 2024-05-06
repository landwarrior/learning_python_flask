import logging
import os
import time
import traceback
import uuid

from config import get_config
from flask import Flask, Response, g, jsonify, request, session, url_for
from flask_minify import Minify
from flask_wtf.csrf import CSRFError, CSRFProtect
from mylogger import UniqueKeyFormatter
from views.top import top_bp
from views.users import users_bp

app = Flask(__name__)


def prepare_logging(app: Flask):
    app.logger.handlers = []
    app.logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = UniqueKeyFormatter()
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


app.config.from_object(get_config())
app.json.ensure_ascii = False
Minify(app=app, html=True, js=True, cssless=True)
prepare_logging(app)


def static_file_with_mtime(filename):
    file_path = os.path.join(app.root_path, "static", filename)
    try:
        mtime = os.path.getmtime(file_path)
    except OSError:
        return url_for("static", filename=filename)
    mtime_str = f"?v={mtime}"
    full_path = url_for("static", filename=filename) + mtime_str
    return full_path


app.jinja_env.globals["url_for_with_mtime"] = static_file_with_mtime


@app.before_request
def before_request():
    if "static" not in request.url:
        g.start_time = time.time()
        # UUID4 を 16 進数にして、 7 文字分だけ使う
        g.unique_key = uuid.uuid4().hex[0:7]
        data = request.get_json(silent=True)
        header = str(request.headers).strip().replace("\r", "").replace("\n", ", ")
        app.logger.info(f"[URL] {request.method} {request.url} [DATA] {data} [HEADER] {header}")


@app.after_request
def after_request(response: Response):
    try:
        duration = time.time() - g.start_time
        app.logger.info(f"[RESPONSE] [STATUS] {response.status_code} [JSON] {response.json} [{duration: .5f} sec]")
    except Exception:
        pass
    finally:
        return response


CSRFProtect(app)


@app.errorhandler(CSRFError)
def handle_exception_error(e):
    app.logger.error(traceback.format_exc())
    app.logger.info(f"session: {session}")
    app.logger.info(f"Unhandled exception: {e}")
    return jsonify({"code": 500, "message": "Internal Server Error"}), 500


app.register_blueprint(top_bp)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)
