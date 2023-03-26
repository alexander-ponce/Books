from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import author_model, book_model

@app.route("/add_book")
def books_page():
    
    all_books= book_model.Books.get_all_books()

    return render_template("create_book.html", all_books=all_books )

@app.route("/create_book", methods=["POST"])
def create_book():
    
    book_id = book_model.Books.save_book(request.form)

    return redirect ('/add_book')


@app.route('/book/<int:id>')
def show_book(id):
    data = {
        "id":id
    }
    return render_template('show_book.html', book=book_model.Books.get_by_id(data), unfavorited_authors=author_model.Authors.unfavorited_authors(data))

@app.route('/fave/author',methods=['POST'])
def fave_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author_model.Authors.add_favorite(data)
    return redirect(f"/book/{request.form['book_id']}")
