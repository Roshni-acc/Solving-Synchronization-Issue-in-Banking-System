import threading
from database import db
from models import User
from bank import BankAccount
from app import app

# Function to simulate deposit
def deposit_money(user_id, amount):
    with app.app_context():
        user = db.session.get(User, user_id)  # ✅ Fix deprecated .get()
        if user:
            account = BankAccount(user)
            account.deposit(amount)

# Function to simulate withdrawal
def withdraw_money(user_id, amount):
    with app.app_context():
        user = db.session.get(User, user_id)  # ✅ Fix deprecated .get()
        if user:
            account = BankAccount(user)
            account.withdraw(amount)

if __name__ == "__main__":
    with app.app_context():
        # Fetch an existing user
        user = User.query.first()
        if not user:
            print("❌ No users found in the database!")
            exit()

        user_id = user.id
        print(f"Starting transactions for user: {user.username} (Initial balance: ${user.balance})")

        # Start deposit and withdrawal at the same time
        deposit_thread = threading.Thread(target=deposit_money, args=(user_id, 200))
        withdraw_thread = threading.Thread(target=withdraw_money, args=(user_id, 100))

        # Start both transactions simultaneously
        deposit_thread.start()
        withdraw_thread.start()

        # Wait for both threads to finish
        deposit_thread.join()
        withdraw_thread.join()

        # Fetch updated balance
        user = db.session.get(User, user_id)
        print(f"🎯 Final balance for {user.username}: ${user.balance}")

