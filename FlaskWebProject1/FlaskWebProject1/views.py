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


@app.before_request
def before_request():
    # セッションにusernameが保存されている（= ログイン済み）
    if session.get('username') is not None:
        return None
    ## リクエストがログインに関するもの
    if request.path == '/login':
        return None
    ## よく分からんので確認用
    if request.path == '/home':
        return None
    ## ログインされていなければリダイレクト
    return redirect(url_for('login'))


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

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