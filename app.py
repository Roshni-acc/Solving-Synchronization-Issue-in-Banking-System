from flask import Flask, render_template, request, redirect, session, flash
from database import db
from models import User
from bank import BankAccount
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect('/register')

        # Generate account number
        account_number = User.generate_account_number()
        user = User(username=username, account_number=account_number)
        user.set_password(password)

        # Save to database
        db.session.add(user)
        db.session.commit()

        # Store user info in session (for displaying in the dashboard)
        session['user_id'] = user.id
        session['username'] = user.username
        session['account_number'] = user.account_number
        session['balance'] = user.balance

        flash(f'Registration successful! Your Account Number: {user.account_number}', 'success')
        return redirect('/dashboard')  # ✅ Redirect to dashboard after registration

    return render_template('register.html')  # Show register form

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard', 'warning')
        return redirect('/login')

    return render_template('dashboard.html', 
                           username=session['username'], 
                           account_number=session['account_number'], 
                           balance=session['balance'])

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        flash('Please log in to deposit money.', 'warning')
        return redirect('/login')

    amount = float(request.form['amount'])
    user = User.query.get(session['user_id'])

    if user:
        account = BankAccount(user)
        account.deposit(amount)

        # Update session
        session['balance'] = user.balance
        flash(f'Successfully deposited ${amount}', 'success')

    return redirect('/dashboard')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        flash('Please log in to withdraw money.', 'warning')
        return redirect('/login')

    amount = float(request.form['amount'])
    user = User.query.get(session['user_id'])

    if user:
        account = BankAccount(user)
        account.withdraw(amount)

        # Update session
        session['balance'] = user.balance
        flash(f'Successfully withdrew ${amount}', 'success')

    return redirect('/dashboard')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['account_number'] = user.account_number
            session['balance'] = user.balance

            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid username or password', 'danger')
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # ✅ Clears all session data
    flash('You have been logged out.', 'info')
    return redirect('/')
