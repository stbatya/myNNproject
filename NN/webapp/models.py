import db
class User(db.Model):
    id = db.Column(db.integer, primary_key=True)
    email = db.Column(db.string(100),unique=True)
    password = db.Column(db.string(100))
    name = db.Column(db.string(100))
