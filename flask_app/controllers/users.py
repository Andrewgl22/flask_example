# import flask so we can use it
from flask import Flask, render_template, request, redirect, session
from flask_app.models.user import User
from flask_app import app

@app.route('/')
def index():
    return 'first end-point'

@app.route('/route2')
def route2():
    return 'route 2'

@app.route('/<str>/<int:id>')
def string_route(str,id):
    return f"{str}{id}"

@app.route('/html')
def html_page():
    session['user'] = 'Cool Person' 
    users = User.get_all()
    return render_template('index.html', users=users)

@app.route('/user/new')
def user_form():
    return render_template('form.html')

@app.route('/user', methods=['POST'])
def create_user():
    print('this is the form data:', request.form)
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