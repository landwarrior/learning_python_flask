import logging
import os
import time
import uuid

from config import get_config
from flask import Flask, Response, g, render_template, request, session, url_for

app = Flask(__name__)


class UniqueKeyFormatter(logging.Formatter):
    """カスタムログフォーマット."""

    def format(self, record):
        """ログフォーマットに unique_key を追加して出力できるようにする."""
        try:
            record.unique_key = g.unique_key
        except Exception:
            record.unique_key = ""
        return super().format(record)


def prepare_logging(app: Flask):
    app.logger.handlers = []
    app.logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = UniqueKeyFormatter(app.config.get("LOG_FORMAT", ""))
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


app.config.from_object(get_config())
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


@app.route("/")
def home():
    session["hoge"] = "fuga"
    return render_template("index.jinja")


if __name__ == "__main__":
    app.run(debug=True)
