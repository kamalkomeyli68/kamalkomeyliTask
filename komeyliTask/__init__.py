__author__ = 'kamal'

__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
app = Flask('komeyliTask')
app.config['SECRET_KEY'] = 'random'
app.debug = True
toolbar = DebugToolbarExtension(app)
from komeyliTask.controllers import *