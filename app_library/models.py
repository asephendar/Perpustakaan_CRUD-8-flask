from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/library_isekai'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Categories(db.Model):
    id_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    book=db.relationship('Books', backref='category', lazy=True)

class Books(db.Model):
    id_book = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    book_author=db.relationship('BookAuthors', backref='book', lazy=True)
    transaction_detail=db.relationship('TransactionDetails', backref='book', lazy=True)

class Authors(db.Model):
    id_author = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    year_birth = db.Column(db.Integer, nullable=False)
    book_author=db.relationship('BookAuthors', backref='author', lazy=True)

class BookAuthors(db.Model):
    id_book_author = db.Column(db.Integer, primary_key=True)
    id_book = db.Column(db.Integer, db.ForeignKey('books.id_book'), nullable=False)
    id_author = db.Column(db.Integer, db.ForeignKey('authors.id_author'), nullable=False)

class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        CheckConstraint("user_type IN ('admin', 'member')", name='user_type_check'),
    )
    transaction_member=db.relationship('Transactions', foreign_keys='Transactions.id_member',  backref='member', lazy=True)
    transaction_admin=db.relationship('Transactions', foreign_keys='Transactions.id_admin', backref='admin', lazy=True)
    
    def is_active(self):
        return True
    def get_id(self):
        return str(self.id_user)
    def is_authenticated(self): # ini Cookies
        return True

class Transactions(db.Model):
    id_transaction = db.Column(db.Integer, primary_key=True)
    id_admin = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    id_member = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    borrowing_date = db.Column(db.Date, nullable=False)
    transaction_detail=db.relationship('TransactionDetails', backref='transaction', lazy=True)

class TransactionDetails(db.Model):
    id_transaction_detail = db.Column(db.Integer, primary_key=True)
    id_transaction = db.Column(db.Integer, db.ForeignKey('transactions.id_transaction'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('books.id_book'), nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    days_late = db.Column(db.Integer, default=None)
    status_late = db.Column(db.Boolean, default=False) 