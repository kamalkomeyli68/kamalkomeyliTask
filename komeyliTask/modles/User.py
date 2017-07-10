from komeyliTask import db


class user(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   email = db.Column(db.String(100))
   name = db.Column(db.String(100))
   family = db.Column(db.String(100))


def __init__(self, name, email, family):
   self.name = name
   self.email = email
   self.family = family

def save(user):
    db.session.add(user)
    db.session.commit()
