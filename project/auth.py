from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Users
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = Users.query.filter_by(Email=email).first()

    if user:
        if check_password_hash(user.Password,password):
            login_user(user, remember=remember)
            flash("logged in successfully")
            return redirect(url_for('main.profile'))
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

    elif  user == None:
        flash('Account not exists. Please Sign Up')
        return redirect(url_for('auth.signup'))

    return render_template("login.html", user=current_user)




@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    age= request.form.get("age")

    user = Users.query.filter_by(Email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.login'))

    elif not email and not name and not password:
        flash('Email address already exists.')
        return redirect (url_for('auth.signup'))

    else:
        new_user = Users(Email=email, Name=name, Password=generate_password_hash(password, method='sha256', ), admin= False)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return redirect(url_for('auth.login'))

@auth.route("/admin")
def admin():
    return render_template("adminlogin.html")

@auth.route("/admin", methods=["POST"])
def admin_login():
    email = request.form.get("email")
    password = request.form.get("password")
    admin_user=Users.query.filter_by(Email=email).first()
    remember =  True if request.form.get('remember') else False


    if admin_user!= None:
        if admin_user.admin and check_password_hash(admin_user.Password, password):
            login_user(admin_user, remember=remember)
            flash('Logged in successfully!', category='success')
            return render_template("admin.html")
        else:
            flash("Please enter the correct details")
            return redirect(url_for('auth.admin_login'))

    elif admin_user is None:
                flash("you are not an admin!")
                return redirect(url_for('auth.admin_login'))

    return render_template("adminlogin.html", admin_user=current_user)




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))