from flask.ext.wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import *
from komeyliTask import app, db, redis_store
from flask import  request, flash, url_for, redirect, render_template
from komeyliTask.modles.User import user, save, checkExistUser, checkUserlogin, getUserObj
from komeyliTask.controllers.loginUser import *
from komeyliTask.controllers.validationAddress import *


app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
loginUserClass = loginUser()
validationAddressClass = validatoinAddress()

class CreateLoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired("این فیلد الزامی است.")])
    password = StringField('password', validators=[DataRequired("این فیلد الزامی است.")])

class CreateRegisterForm(FlaskForm):
    name =  StringField('name', validators=[DataRequired("این فیلد الزامی است.")])
    family =  StringField('family', validators=[DataRequired("این فیلد الزامی است.")])
    email =  StringField('email', validators=[DataRequired("این فیلد الزامی است.")])
    password = PasswordField('password',[DataRequired("این فیلد الزامی است."),EqualTo('confirm', message='کلمه عبور و تکرار آن با یکدیگر منطبق نیست')])
    confirm = PasswordField('Repeat password')

class CreateProfileForm(FlaskForm):
    name =  StringField('name', validators=[DataRequired("این فیلد الزامی است.")])
    family =  StringField('family', validators=[DataRequired("این فیلد الزامی است.")])
    email =  StringField('email', validators=[DataRequired("این فیلد الزامی است.")])
    # password = PasswordField('password',[EqualTo('confirm', message='کلمه عبور و تکرار آن با یکدیگر منطبق نیست')])



@app.route('/', methods=['GET'])
def start():
    loginForm = CreateLoginForm(request.form)
    registerForm = CreateRegisterForm(request.form)

    return render_template('user/index.html' , registerForm = registerForm ,loginForm = loginForm)

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
def profile(self=None):
    if loginUserClass.checkLoginUser():
        profileForm = CreateProfileForm(request.form)
        if request.method == 'POST' and profileForm.validate():
            id = loginUserClass.getCurrentUserId()
            name = request.form['name']
            email = request.form['email']
            family = request.form['family']
            password = request.form['password']
            confirm = request.form['confirm']

            address = request.form['address']
            userObj = user.query.get(id)
            if (validationAddressClass.checkValidAddress(address=address)):
                userObj.name = name
                userObj.family = family
                userObj.email = email
                userObj.address = address
                if password != "":
                    if confirm == password:
                        userObj.password = generate_password_hash(password)
                    else:
                        flash('کلمه عبور و تکرار آن با هم منطبق نیست','error')
                        return redirect(url_for('profile'), code=302)
                db.session.commit()
                flash('ثبت انجام شد...','success')
            else:
                flash('آدرس وارد شده معتبر نیست...','error')
            return redirect(url_for('profile'), code=302)



        return render_template('user/profile.html', profileForm=profileForm, userObj = getUserObj(loginUserClass.getCurrentUserId()))
    else:
        return redirect(url_for('start'))

@app.route('/register', methods=['POST'])
def register():
    loginForm = CreateLoginForm(request.form)
    registerForm = CreateRegisterForm(request.form)
    if request.method == 'POST' and registerForm.validate():
        name = request.form['name']
        email = request.form['email']
        family = request.form['family']
        password = request.form['password']
        if not checkExistUser(email):
            User = user(name=name, email=email, family=family, password=generate_password_hash(password))
            save(User)
            flash('کاربر گرامی با تشکر از ورود شما به سامانه...!')
            redis_store.__setitem__("user_Id",User.id)
            redis_store.__setitem__("user_Name",User.name)
            return redirect(url_for('profile'), code=302)
        else:
            flash('این ایمیل قبلا ثبت نام کرده است!')
            return redirect(url_for('start'))
    return render_template('user/index.html' , registerForm = registerForm, loginForm = loginForm)


@app.route('/login', methods=['POST'])
def login():
    loginForm = CreateLoginForm(request.form)
    registerForm = CreateRegisterForm(request.form)
    if request.method == 'POST' and loginForm.validate():
        email = request.form['email']
        password = request.form['password']
        if checkUserlogin(email=email,password=password):
            flash('کاربر گرامی با تشکر از ورود شما به سامانه...!')
            return redirect(url_for('profile'), code=302)
        else:
            flash('نام کاربری و کلمه عبور اشتباه است.')
            return redirect(url_for('start'), code=302)
    return render_template('user/index.html' , registerForm = registerForm, loginForm = loginForm)
