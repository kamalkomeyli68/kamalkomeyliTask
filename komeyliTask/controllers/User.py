from flask.ext.wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import *
from komeyliTask import app, db, redis_store
from flask import  request, flash, url_for, redirect, render_template
from komeyliTask.modles.User import user, save
from komeyliTask.controllers.loginUser import *

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
loginUserClass = loginUser()

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
    if loginUserClass.checkLoginUser():
        return render_template('user/dashboard.html' )
    else:
        return redirect(url_for('start'))

@app.route('/logout', methods=['GET'])
def logout():
    redis_store.__delitem__('user_Id')
    return redirect(url_for('start'))

@app.route('/profile', methods=['GET','POST'])
def profile():
    if loginUserClass.checkLoginUser():
        registerForm = CreateRegisterForm(request.form)
        if request.method == 'POST' and registerForm.validate():
            id = request.form['id']
            name = request.form['name']
            email = request.form['email']
            family = request.form['family']
            password = request.form['password']
            address = request.form['address']
            userObj = user.query.get(id)
            userObj.address = address
            db.session.commit()
            flash('ثبت انجام شد...')
            return redirect(url_for('profile'), code=302)
        return render_template('user/profile.html')
    else:
        return redirect(url_for('start'))

@app.route('/register', methods=['POST'])
def register():

    registerForm = CreateRegisterForm(request.form)
    if request.method == 'POST' and registerForm.validate():
        name = request.form['name']
        email = request.form['email']
        family = request.form['family']
        password = request.form['password']
        User = user(name=name, email=email, family=family, password=generate_password_hash(password))
        save(User)
        flash('کاربر گرامی با تشکر از ورود شما به سامانه...!')
        redis_store.__setitem__("user_Id",User.id)
        redis_store.__setitem__("user_Name",User.name)
        return redirect(url_for('dashboard'), code=302)

    return render_template('user/index.html' , registerForm = registerForm)
