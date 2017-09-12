
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import escape
from FlaskWebProject1 import app
from FlaskWebProject1 import models

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
    user_name = request.form.get('userid')
    db_data = models.User.get_data(user_name)
    if db_data is not None:
        password = request.form.get('ignitionkey')
        if db_data.password == password:
            session['username'] = user_name
            return redirect(url_for('home'))
        else:
            return render_template(
            'login.html',
            title='Login',
            ispost=True,
            userid=request.form.get('userid'),
            ignitionkey=request.form.get('ignitionkey'),
            year=datetime.now().year,
        )
    else:
        return render_template(
            'login.html',
            title='Login',
            ispost=True,
            userid=request.form.get('userid'),
            ignitionkey=request.form.get('ignitionkey'),
            year=datetime.now().year
        )


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))