from flask import session
from komeyliTask import redis_store


class loginUser() :

    def __init__(self):
        pass

    def checkLoginUser(self):
        try:
            c = redis_store.__getitem__("user_Id").decode("utf-8")
            session["user_Name"] = redis_store.__getitem__("user_Name").decode("utf-8")
            if not c:
                return False
            else:
                return True
        except:
            return False

    def getCurrentUserId(self):
        return redis_store.get("user_Id").decode("utf-8")