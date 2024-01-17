from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybooks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', book_stack=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        b_name = request.form["book"]
        b_author = request.form["author"]
        b_rating = request.form["rating"]
        new_book = Book(title=b_name, author=b_author, rating=b_rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
