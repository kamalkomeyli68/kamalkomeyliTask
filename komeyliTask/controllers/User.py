from flask.ext.wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

__author__ = 'kamal'
from komeyliTask import app
from flask import render_template, request


class CreateLoginForm(FlaskForm):
    text = StringField('username', validators=[DataRequired()])
    text1 = StringField('password', validators=[DataRequired()])

class CreateRegisterForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])

@app.route('/', methods=['GET'])
def start():
    loginForm = CreateLoginForm(request.form)
    registerForm = CreateRegisterForm(request.form)

    return render_template('user/index.html', registerForm = registerForm)

@app.route('/register', methods=['POST'])
def register():
    return render_template('user/index.html')
