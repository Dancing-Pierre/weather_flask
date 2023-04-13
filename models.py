from manage import db


class User(db.Model):
    """
    用户表
    """
    __tablename__ = "user"
    id = db.Column(db.INT, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    identity = db.Column(db.INT)
