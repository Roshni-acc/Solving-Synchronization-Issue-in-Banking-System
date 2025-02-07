import threading
import time
from database import db
from models import User

class BankAccount:
    def __init__(self, user):
        self.user = user
        self.lock = threading.Lock()

    def deposit(self, amount):
        if amount > 0:
            print(f"Depositing {amount} to {self.user.username}'s account")
            with self.lock:
                current_balance = self.user.balance
                time.sleep(0.05)
                current_balance += amount
                self.user.balance = current_balance
                db.session.commit()
            print(f"{self.user.username}'s new balance after deposit: {self.user.balance}")

    def withdraw(self, amount):
        if amount > 0:
            with self.lock:
                if self.user.balance >= amount:
                    print(f"Withdrawing {amount} from {self.user.username}'s account")
                    current_balance = self.user.balance
                    time.sleep(0.05)
                    current_balance -= amount
                    self.user.balance = current_balance
                    db.session.commit()
                    print(f"{self.user.username}'s new balance after withdrawal: {self.user.balance}")
                else:
                    print(f"Insufficient funds in {self.user.username}'s account")
