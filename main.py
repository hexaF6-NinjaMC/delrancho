import os, json
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from helper.Forms import CreateUserForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

# ==============---------------SETUP---------------==============
# # Create the Flask Application
app = Flask(__name__)
# Get configs

#     # Fakes
#     # Add Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#     # Get a Secret Key
# app.config['SECRET_KEY'] = 'del_rancho_secret'
# skey = app.config['SECRET_KEY']

    # Legits
    # Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    # Get a Secret Key
app.config['SECRET_KEY'] = os.environ.get('LOGIN_SECRET')
skey = app.config['SECRET_KEY']

# Initialize the database
database = SQLAlchemy(app)
app.app_context().push()
migrate = Migrate(app, database)

# Flask_Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# ==============---------------PAGE RENDERS---------------==============
# Home page
@app.route("/")
def main():
    return render_template('index.html')

# Announcements
@app.route("/announcements")
@login_required
def announcements():
    all_reg_users = Users.query.order_by(Users.date_added)
    return render_template('announcements.html', date=datetime.today().date().strftime('%m-%d-%Y'), users=all_reg_users)

# Birthdays
@app.route("/birthdays")
@login_required
def birthdays():
    all_reg_users = Users.query.order_by(Users.date_added)
    today = datetime.today()
    return render_template('birthdays.html', today=today, users=all_reg_users)

# Tests / Quizzes
@app.route("/testing")
@login_required
def testing():
    all_reg_users = Users.query.order_by(Users.date_added)
    with open('./static/assets/json/menu_items.json', 'r') as menu_file_json:
        menu_file = []
        load_file = json.load(menu_file_json)
        menu_file.append(load_file['menu'])
    return render_template('testing.html', users=all_reg_users)

# Delete database records
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)

    try:
        database.session.delete(user_to_delete)
        database.session.commit()
        flash("User deleted successfully.", category="success")
        
    except:
        flash("Whoops! There was an error deleting the user, try again.", category="error")

    return redirect(url_for('dashboard'))

# Create a User page
@app.route('/user/add', methods=['GET', 'POST'])
def create_user():
    name = None
    form = CreateUserForm()

    # Validate Form
    if form.validate():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            # Hash password!
            hashed_pw = generate_password_hash(form.password.data, 'scrypt')
            user = Users(
                fname=form.fname.data,
                lname=form.lname.data,
                birthday=form.birthday.data,
                username=form.username.data,
                password_hash=hashed_pw
            )
            database.session.add(user)
            database.session.commit()
            flash("User created successfully! You may now login.", category="success")
        else:
            flash("That username is already taken. Please choose another.", category="error")
        form.username.data = ''
        form.password.data = ''
        form.password_confirmation.data = ''

        def __repr__(self):
            return '<Name %r>' % self.name
        
    all_reg_users = Users.query.order_by(Users.date_added)
    return render_template('create-user.html', name=name, form=form, users=all_reg_users)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = None
    password = None
    user_to_check = None
    passed = None
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Clear the form
        form.username.data = ''
        form.password.data = ''

        # Lookup User by email
        user_to_check = Users.query.filter_by(username=username).first()
        if user_to_check:
            # Check Hash password!
            passed = check_password_hash(user_to_check.password_hash, password)
            if passed:
                login_user(user_to_check)
                flash("Login successful!", category="success")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect credentials. Try again.", category="error")
                return render_template('login.html', username=username, password=password, form=form, passed=passed)
        else:
            flash("Incorrect credentials. Try again.", category="error")
            return render_template('login.html', username=username, password=password, form=form, passed=passed)
    else:
        return render_template('login.html', username=username, password=password, form=form, passed=passed)

# Create a Dashboard page
@app.route('/dashboard')
@login_required
def dashboard():
    all_reg_users = Users.query.order_by(Users.date_added)
    return render_template('dashboard.html', users=all_reg_users)

# Create Logout page
@app.route('/logout')
@login_required # You can't log out without logging in!
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for('login'))

# ==============---------------IN-PAGE RENDERS---------------==============

# ==============---------------PAGE ERROR HANDLERS---------------==============
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

class Users(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    fname = database.Column(database.String(255), nullable=False)
    lname = database.Column(database.String(255), nullable=False)
    birthday = database.Column(database.DateTime, nullable=False)
    username = database.Column(database.String(12), nullable=False)
    date_added = database.Column(database.DateTime, default=datetime.utcnow)

    # Do some password hashing!
    password_hash = database.Column(database.String(255), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# ==============---------------MAIN EXECUTION---------------==============
# The MAIN way to run the Flask app
if __name__ == "__main__":
	app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

    # OR

	# app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
