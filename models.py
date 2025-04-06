from database import db
from werkzeug.security import generate_password_hash, check_password_hash
import random

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    secondname = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    username = db.Column(db.String(100))  # Can be firstname + secondname
    password_hash = db.Column(db.String(255))
    account_number = db.Column(db.String(20), unique=True)
    balance = db.Column(db.Float, default=0.0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_account_number():
        return str(random.randint(1000000000, 9999999999))

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False


