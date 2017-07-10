from flask.ext.sqlalchemy import SQLAlchemy

__author__ = 'kamal'
__version__ = '0.1'

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask('komeyliTask')
app.config['SECRET_KEY'] = 'random'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/task'
db = SQLAlchemy(app)

app.debug = True


toolbar = DebugToolbarExtension(app)
from komeyliTask.controllers import *