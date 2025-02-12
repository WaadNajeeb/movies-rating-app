from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import re
from flask_login import login_user, login_required, logout_user, current_user
from app.constants.regex import PASSWORD_PATTERN
from app.models.user import User
from app.userschema import UserSchema


auth = Blueprint("auth", __name__, url_prefix="/auth")

user_schema = UserSchema()


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_home'))

@auth.route('/register', methods=['GET', 'POST'])
def post_register():
    if request.method == 'POST':
        session.pop('_flashes', None)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        
        if re.match(PASSWORD_PATTERN, password) is None:
            flash("Password is not valid", "error")
            return render_template('registration.html')
        
        if password != confirmPassword:
            flash("Passwod do not match", "error")
            return render_template('registration.html')
            
        if len(username) < 3:
          flash("Username must be more than 3 characters", "error")
          return render_template('registration.html')
        
        if User.usernameExists(username=username):
          flash("Username is taken already. Try another one.", "error")
          return render_template('registration.html')

        user = User(username=username, email=email, firstname=firstname, lastname=lastname)
        
        # create the password
        user.generate_pass(password = password)
        
        # create the db record    
        user.save()
        
        return redirect(url_for('auth.get_login'))
    
    if current_user.is_authenticated:
      return redirect(url_for('get_home'))
       
    return render_template('registration.html')

@auth.route('/login', methods=['GET', 'POST'])
def get_login():
    session.pop('_flashes', None)
    if request.method == 'POST':
        session.pop('_flashes', None)
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_user_by_username(username=username)
    
        if user and (user.check_pass(password=password)):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            next_page = request.args.get("next_page") # get the url argument
            if next_page :
              return redirect(next_page)
            
            return redirect(url_for('get_home'))
        else:
            flash('Username or password is invalid!', category='error')
            return render_template('login.html')
            
    session.pop('_flashes', None)
    if current_user.is_authenticated:
      return redirect(url_for('get_home'))
       
    return  render_template("login.html")


@auth.get('/check_user')
def check_login_status():
    print("Checking")
    if current_user.is_authenticated:
        return {'LoggedIn': True}
    else:
        flash('You must login in to create a review!', category='info')
        return {'LoggedIn': False}