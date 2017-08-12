"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is a drill.'

import FlaskWebProject1.views
