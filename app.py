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
        firstname = request.form['firstname']
        secondname = request.form['secondname']
        email = request.form['email']
        phone_number = request.form['phone_number']
        gender = request.form['gender']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect('/register')

        username = firstname + secondname

        # Check for duplicate email or username
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect('/register')

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect('/register')

        account_number = User.generate_account_number()
        user = User(
            firstname=firstname,
            secondname=secondname,
            email=email,
            phone_number=phone_number,
            gender=gender,
            username=username,
            account_number=account_number
        )
        user.set_password(password)  

        db.session.add(user)
        db.session.commit()

        flash(f'Registration successful! Your Account Number: {user.account_number}', 'success')
        return redirect('/dashboard')

    return render_template('register.html')



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
        flash(f'Successfully deposited Rs.{amount}', 'success')

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
        email = request.form['email']
        password = request.form['password']

        # Check if user exists with this email
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Set session variables
            session['user_id'] = user.id
            session['username'] = user.firstname + " " + user.secondname
            session['account_number'] = user.account_number
            session['balance'] = getattr(user, 'balance', 0)

            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid email or password', 'danger')
            return redirect('/login')

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()  # ✅ Clears all session data
    flash('You have been logged out.', 'info')
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
