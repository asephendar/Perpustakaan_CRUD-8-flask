from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/library_isekai'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

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

class Authors(db.Model):
    id_author = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(255), nullable=False)
    year_birth = db.Column(db.Integer, nullable=False)

class BookAuthors(db.Model):
    id_book_author = db.Column(db.Integer, primary_key=True)
    id_book = db.Column(db.Integer, db.ForeignKey('books.id_book'), nullable=False)
    id_author = db.Column(db.Integer, db.ForeignKey('authors.id_author'), nullable=False)

class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
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

class TransactionDetails(db.Model):
    id_transaction_detail = db.Column(db.Integer, primary_key=True)
    id_transaction = db.Column(db.Integer, db.ForeignKey('transactions.id_transaction'), nullable=False)
    id_book = db.Column(db.Integer, db.ForeignKey('books.id_book'), nullable=False)
    return_date = db.Column(db.Date, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return {'message': 'You are already logged in'}
    
    username = request.headers.get('username')
    password = request.headers.get('password')

    user = Users.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return {'message': 'Login successful'}
    else:
        return {'message': 'Invalid username or password'}, 401

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return {'message': 'Logout successful'}

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    name = current_user.username
    return {'message': f'Welcome, {name}!'}

@app.route('/categories', methods=['GET'])
def view_category():
    data = Categories.query.order_by(Categories.id_category.desc()).all()
    categories_list = []
    for el in data:
        categories_list.append({
            'id_category': el.id_category,
            'name': el.name,
            'description': el.description
        })
    return {'Category': categories_list}

if __name__ == '__main__':
    app.run(debug=True)