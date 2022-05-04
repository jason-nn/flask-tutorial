from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask:flask@localhost/flask_tutorial'

db = SQLAlchemy(app)


class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    likes = db.Column(db.Integer(), default=0, nullable=False)

    def __init__(self, title, author, likes):
        self.title = title
        self.author = author
        self.likes = likes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books', methods=['GET'])
def get_books():
    books = Books.query.all()
    return json.dumps(books)


@app.route('/books', methods=['POST'])
def post_books():
    data = request.get_json()
    book = Books(
        title=data['title'],
        author=data['author'],
        likes=data['likes']
    )
    db.session.add(book)
    db.session.commit()
    return {
        'status': 'success'
    }


if __name__ == '__main__':
    app.run(debug=True)
