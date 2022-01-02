from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    refresh_token = db.Column(db.String(200))

    def __init__(self, username, email, password, refresh_token):
        self.username = username
        self.email = email
        self.password = sha256_crypt.encrypt(password)
        self.refresh_token = refresh_token

    def decrypt(input, db_passw):
        return sha256_crypt.verify(input, db_passw) #veerifying password input is = to encrypted password in db
        #returns true or false