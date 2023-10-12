from flask import Flask, render_template, request, redirect, session
from flask_app.models.book import Book
from flask_app.models.user import User
from flask_app import app

@app.route('/book/new')
def book_form():
    return render_template('book_form.html')

@app.route('/book', methods=['POST'])
def submit_book():
    data = {
        "title":request.form['title'],
        "author":request.form['author'],
        "num_pages":request.form['num_pages'],
        "user_id":session['user_id']
    }
    Book.save(data)
    return redirect('/dashboard') 

@app.route('/book/<int:id>')
def one_book(id):
    data = {
        "id":id
    }
    one_book = Book.get_book_by_id(data)
    users_who_favorited = User.get_all_users_who_favorited({"id":id})
    return render_template('show.html', book=one_book, users=users_who_favorited)

# get one book and render edit page with form
@app.route('/book/<int:id>/edit')
def book_edit_form(id):
    data = {
        "id":id
    }
    book = Book.get_book_by_id(data)
    return render_template('edit_form.html',book=book)

@app.route('/book/update', methods=['POST'])
def book_update():
    data = {
        "id":request.form['id'],
        "title":request.form['title'],
        "author":request.form['author'],
        "num_pages":request.form['num_pages']
    }
    Book.update(data)
    return redirect('/dashboard')

@app.route("/book/<int:id>/delete")
def delete_book(id):
    data = {
        "id":id
    }
    Book.delete(data)
    return redirect('/dashboard')

@app.route("/favorite/<int:id>")
def favorite_book(id):
    data = {
        "user_id": session['user_id'],
        "book_id": id 
    }
    Book.add_favorite(data)
    return redirect('/dashboard')








    
    

