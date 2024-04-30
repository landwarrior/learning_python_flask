import logging
import time
import uuid

from api import api_bp
from config import get_config
from flask import Flask, Response, g, request

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
    return response


app.register_blueprint(api_bp)


if __name__ == "__main__":
    app.run(debug=True)
