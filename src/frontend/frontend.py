import os

from flask import Flask, render_template, url_for

app = Flask(__name__)


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


@app.route("/")
def home():
    return render_template("index.jinja")


if __name__ == "__main__":
    app.run(debug=True)
