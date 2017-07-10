from flask.ext.wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import *
from komeyliTask import app
from flask import  session,request, flash, url_for, redirect, render_template


app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

class CreateLoginForm(FlaskForm):
    text = StringField('username', validators=[DataRequired()])
    text1 = StringField('password', validators=[DataRequired()])

class CreateRegisterForm(FlaskForm):
    name =  StringField('name', validators=[DataRequired("این فیلد الزامی است.")])
    family =  StringField('family', validators=[DataRequired("این فیلد الزامی است.")])
    email =  StringField('email', validators=[DataRequired("این فیلد الزامی است.")])
    password = PasswordField('password',[DataRequired("این فیلد الزامی است."),EqualTo('confirm', message='کلمه عبور و تکرار آن با یکدیگر منطبق نیست')])
    confirm = PasswordField('Repeat password')

@app.route('/', methods=['GET'])
def start():
    loginForm = CreateLoginForm(request.form)
    registerForm = CreateRegisterForm(request.form)

    return render_template('user/index.html' , registerForm = registerForm)

@app.route('/dashboard', methods=['GET'])
def dashboard():

    return render_template('user/dashboard.html' )

@app.route('/register', methods=['POST'])
def register():
    registerForm = CreateRegisterForm(request.form)
    a = registerForm.validate()
    if request.method == 'POST' and registerForm.validate():
        flash('کاربر گرامی با تشکر از ورود شما به سامانه...!')
        return redirect(url_for('dashboard'), code=302)

    return render_template('user/index.html' , registerForm = registerForm)
