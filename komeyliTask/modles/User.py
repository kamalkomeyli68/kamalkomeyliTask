from werkzeug.security import generate_password_hash, check_password_hash
from komeyliTask import db


class user(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   email = db.Column(db.String(100))
   name = db.Column(db.String(100))
   family = db.Column(db.String(100))
   password = db.Column(db.String(100))
   address = db.Column(db.Text)

def __init__(self, name, email, family,password,address=""):
   self.name = name
   self.email = email
   self.family = family
   self.password = password
   self.address = address

def save(user):
    db.session.add(user)
    db.session.commit()

def set_password(self, password):
    self.password = generate_password_hash(password)

def check_password(id, password):
    query = user.query.filter_by(id = id)
    results = query.first()
    print(results.password)
    print(check_password_hash(str(results.password), str(password)))