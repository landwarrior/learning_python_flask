import logging
import time

from api import api_bp
from flask import Flask, Response, g, request

app = Flask(__name__)


def prepare_logging(app: Flask):
    app.logger.handlers = []
    app.logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s](%(name)s) %(message)s [in %(pathname)s:%(lineno)d]")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


prepare_logging(app)


@app.route("/status")
def home():
    return "200 OK"


@app.before_request
def before_request():
    g.start_time = time.time()
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
