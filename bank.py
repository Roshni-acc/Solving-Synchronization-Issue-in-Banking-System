import threading
import time
from database import db
from models import User
from flask import flash, Flask

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
        """ Handles withdrawal transactions and prevents overdrawing """
        with self.lock:
            print(f"🔴 [WITHDRAW] {self.user.username} is trying to withdraw ${amount}...")
            time.sleep(0.05)  # Simulate processing delay

            # Ensure we have the latest balance before withdrawing
            db.session.refresh(self.user)

            if self.user.balance >= amount:
                self.user.balance -= amount
                db.session.commit()
                print(f"✅ [WITHDRAW SUCCESS] New balance for {self.user.username}: ${self.user.balance}")
                return True  # Successful withdrawal
            else:
                # print(f"❌ [WITHDRAW FAILED] Insufficient funds for {self.user.username}")
                # flash("❌ Withdrawal failed: Insufficient balance!", "danger")
                return False  # Failed withdrawal due to insufficient funds