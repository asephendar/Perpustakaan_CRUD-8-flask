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

class Books(db.Model):
    id_book = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    category = db.relationship('Categories', backref=db.backref('books', lazy=True))

class Authors(db.Model):
    id_author = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    year_birth = db.Column(db.Integer, nullable=False)

class BookAuthors(db.Model):
    id_book_author = db.Column(db.Integer, primary_key=True)
    id_book = db.Column(db.Integer, db.ForeignKey('books.id_book'), nullable=False)
    id_author = db.Column(db.Integer, db.ForeignKey('authors.id_author'), nullable=False)
    author = db.relationship('Authors', backref=db.backref('book_authors', lazy=True))
    book = db.relationship('Books', backref=db.backref('book_authors', lazy=True))

class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        CheckConstraint("user_type IN ('admin', 'member')", name='user_type_check'),
    )
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
    member = db.relationship('Users', foreign_keys=id_member, backref=db.backref('transactions_as_member', lazy=True))
    admin = db.relationship('Users', foreign_keys=id_admin, backref=db.backref('transactions_as_admin', lazy=True))

class TransactionDetails(db.Model):
    id_transaction_detail = db.Column(db.Integer, primary_key=True)
    id_transaction = db.Column(db.Integer, db.ForeignKey('transactions.id_transaction'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('books.id_book'), nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    days_late = db.Column(db.Integer, default=None)
    status_late = db.Column(db.Boolean, default=False) 
    transaction = db.relationship('Transactions', backref=db.backref('transaction_details', lazy=True))
    book = db.relationship('Books', backref=db.backref('transaction_details', lazy=True))