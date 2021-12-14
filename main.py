import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-book-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()

book = Books(id=1, title='Harry Potter', author='J. K. Rowling', rating=9.5)
db.session.add(book)
db.session.commit()


# db = sqlite3.connect('book-collection.db')
# cursor = db.cursor()
# # cursor.execute('CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) '
# #                'NOT NULL, rating FLOAT NOT NULL)')
#
# cursor.execute('INSERT INTO books VALUES(1, "Harry Potter", "J. K. Rowling", "9.3")')
# db.commit()


class AddForm(FlaskForm):
    book_name = StringField(label='Book Name', validators=[DataRequired()])
    book_author = StringField(label='Book Author', validators=[DataRequired()])
    book_rating = StringField(label='Book Rating e.g, 8/10', validators=[DataRequired()])
    add_book = SubmitField(label='Add Book')


all_books = []


@app.route('/')
def home():
    return render_template('index.html', all_books=all_books, number_of_inventory=len(all_books))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddForm()
    form.validate_on_submit()
    if request.method == 'POST' and form.validate_on_submit():
        book_data = {
            'title': form.book_name.data,
            'author': form.book_author.data,
            'rating': form.book_rating.data
        }
        all_books.append(book_data)
        return render_template('index.html', all_books=all_books)
    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
