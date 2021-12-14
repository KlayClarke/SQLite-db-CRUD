import os
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')


class AddForm(FlaskForm):
    book_name = StringField(label='Book Name', validators=[DataRequired()])
    book_author = StringField(label='Book Author', validators=[DataRequired()])
    book_rating = StringField(label='Book Rating e.g, 8/10', validators=[DataRequired()])
    add_book = SubmitField(label='Add Book')


all_books = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/add", methods=['GET', 'POST'])
def add():
    book_inventory = all_books
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
