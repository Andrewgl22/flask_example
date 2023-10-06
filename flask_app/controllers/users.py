# import flask so we can use it
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.book import Book
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    # confirm password and confirm password fields match
    if request.form['password'] != request.form['confirm_pw']:
        flash('Password and Confirm Password do not match! Do not pass go. Do not collect $200.')
        return redirect('/')
    data = {"email": request.form['email']}
    user_in_db = User.get_one_by_email(data)
    if user_in_db:
        flash("Email already exists!")
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash,
    }

    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form['email']}
    user_in_db = User.get_one_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    # users = User.get_all()
    books = Book.get_books_w_creator()
    user = User.get_one_by_id({"id":session['user_id']})
    return render_template('index.html', books=books, user=user)

@app.route('/user/new')
def user_form():
    return render_template('form.html')

@app.route('/user', methods=['POST'])
def create_user():
    print('this is the form data:', request.form)

    if not User.validate_user(request.form):
        return redirect('/user/new')

    data = {
        "username":request.form['username'],
        "email":request.form['email'],
        "age":request.form['age'],
        "country":request.form['country']
    }
    User.save(data)
    return redirect('/html')

@app.route('/user/<int:id>')
def one_user(id):
    data = {
        "id":id
    }
    user = User.get_one_by_id(data)
    return render_template('one_user.html',user=user)

# sends us to the edit form with one user's information
@app.route('/user/<int:id>/edit')
def edit_form(id):
    data = {
        "id":id
    }
    user = User.get_one_by_id(data)
    return render_template('update_form.html',user=user)

# update a user
@app.route('/user/<int:id>', methods=['POST'])
def update(id):
    data = {
        "id":id,
        "username":request.form['username'],
        "email":request.form['email'],
        "age":request.form['age'],
        "country":request.form['country']
    }
    User.update(data)
    return redirect('/html')

@app.route('/user/<int:id>/delete')
def delete(id):
    data = {
        "id":id
    }
    User.delete(data)
    return redirect('/html')

@app.route('/user_list')
def user_list():
    users = User.get_users_w_books()
    return render_template('user_list.html',users=users)