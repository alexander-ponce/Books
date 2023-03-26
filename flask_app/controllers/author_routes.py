from flask_app import app
from flask import Flask, render_template, request, redirect, session
from flask_app.models import author_model, book_model

@app.route('/')
def index():
    return redirect('/authors')

@app.route("/authors")
def home_page():
    
    all_authors= author_model.Authors.get_all_authors()

    return render_template("create_author.html", all_authors=all_authors )

@app.route("/create_author", methods=["POST"])
def create_author():
    data = {
        "name": request.form['name']
    }
    author_id = author_model.Authors.save_author(data)
    return redirect('/authors')

    # author_id = author_model.Authors.save_author(request.form)
    # return redirect ('/authors')


@app.route('/author_page/<int:id>')
def author_page(id):
    data={
        'id':id
    }

    author_name = author_model.Authors.get_by_id(data)
    unfave_books = book_model.Books.unfavorited_books(data)

    return render_template ('show_author.html', author_name=author_name, unfave_books = unfave_books )

@app.route('/join/book',methods=['POST'])
def join_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author_model.Authors.add_favorite(data)
    return redirect(f"/author_page/{request.form['author_id']}")

if __name__ == "__main__":
    app.run(debug=True)