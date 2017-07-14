from flask import session
from komeyliTask import redis_store


class loginUser() :

    def __init__(self):
        pass

    def checkLoginUser(self):
        try:
            c = redis_store.__getitem__("user_Id")
            session["user_Name"] = redis_store.__getitem__("user_Name")
            if not c:
                return False
            else:
                return True
        except:
            return False
