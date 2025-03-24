import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)


# Database Configuration
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Book Model
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


# Initialize Database
with app.app_context():
    db.create_all()


# Home Route
@app.route('/')
def home():
    all_books = Book.query.order_by(Book.title).all()
    return render_template('index.html', all_books=all_books)


# Add Route
@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            rating=float(request.form["rating"])
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get(id)

    if request.method == 'POST':
        new_rating = request.form.get("erating")

        if book:
            book.rating = new_rating
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('edit.html', book=book)


@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    with app.app_context():
        book_to_delete = db.session.get(Book, id)
        if book_to_delete:
            db.session.delete(book_to_delete)
            db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
