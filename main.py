from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from book_db import Book, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

all_books = []


@app.route('/')
def home():
    with app.app_context():
        all_books_db = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
        return render_template('index.html', all_books=all_books_db)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']
        with app.app_context():
            book = Book(title=title, author=author, rating=rating)
            db.session.add(book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit<int:index>', methods=['POST', 'GET'])
def edit(index):
    with app.app_context():
        book = db.session.execute(db.select(Book).where(Book.id == index)).scalar()
        if request.method == 'POST':
            rating = request.form['new_rating']
            book.rating = rating
            db.session.commit()
        return render_template('edit_rating.html', book=book)

@app.route('/delete')
def delete():
    book_id = request.args.get('ind')

    #DELETE a record
    book_to_delete = db.get_or_404(Book, book_id)
    #Alternative way to select the book to delete
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)
