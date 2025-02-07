from database import db
from werkzeug.security import generate_password_hash, check_password_hash
import random

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    account_number = db.Column(db.String(10), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_account_number():
        return str(random.randint(1000000000, 9999999999))
