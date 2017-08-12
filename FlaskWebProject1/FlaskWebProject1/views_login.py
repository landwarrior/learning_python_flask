
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from FlaskWebProject1 import app


@app.route('/login', methods=['GET'])
def login():
    """Renders the login page."""
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year,
    )

@app.route('/login', methods=['POST'])
def try_login():
    """Try login"""
    return render_template(
        'login.html',
        title='Login',
        ispost=True,
        userid=request.form.get('userid'),
        ignitionkey=request.form.get('ignitionkey'),
        year=datetime.now().year,
    )