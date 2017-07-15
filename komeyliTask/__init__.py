from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.redis import FlaskRedis

__author__ = 'kamal'
__version__ = '0.1'

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask('komeyliTask')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///komeyliTask.users'
app.config['SECRET_KEY'] = 'random'
db = SQLAlchemy(app)
db.init_app(app)
app.debug = True
redis_store = FlaskRedis(app)


toolbar = DebugToolbarExtension(app)
from komeyliTask.controllers import *