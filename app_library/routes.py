from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from app_library.models import app, db, Categories, Books, Authors, BookAuthors, Users, Transactions, TransactionDetails

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
@login_required
def get_categories():
    if current_user.user_type == 'admin':
        data = Categories.query.order_by(Categories.id_category.desc()).all()
        categories_list = []
        for el in data:
            categories_list.append({
                'id_category': el.id_category,
                'name': el.name,
                'description': el.description
            })
        return {'categories': categories_list}
    else:
        return {'message': 'Access denied'}, 403

@app.route('/categories', methods=['POST'])
@login_required
def create_category():
    if current_user.user_type == 'admin':
        data = Categories(
            name=request.form['name'],
            description=request.form['description']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Category created successfully'}, 201
    else:
        return {'message': 'Access denied'}, 403

@app.route('/categories/<int:id_category>', methods=['PUT'])
@login_required
def update_category(id_category):
    if current_user.user_type == 'admin':
        data = Categories.query.get(id_category)
        if data:
            data.name = request.form['name']
            data.description = request.form['description']
            db.session.commit()
            return {'message': 'Category updated successfully'}
        else:
            return {'message': 'Category not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/categories/<int:id_category>', methods=['DELETE'])
@login_required
def delete_category(id_category):
    if current_user.user_type == 'admin':
        data = Categories.query.get(id_category)
        if data:
            db.session.delete(data)
            db.session.commit()
            return {'message': 'Category deleted successfully'}
        else:
            return {'message': 'Category not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/books', methods=['GET'])
@login_required
def view_books():
    data = Books.query.order_by(Books.id_book.desc()).all()
    books_list = []
    for el in data:
        books_list.append({
            'id_book': el.id_book,
            'title': el.title,
            'year': el.year,
            'total_pages': el.total_pages,
            'id_category': el.id_category,
            'category': {
                'name': el.category.name,
                'description': el.category.description
            }
        })
    return {'books': books_list}

@app.route('/books', methods=['POST'])
@login_required
def create_book():
    if current_user.user_type == 'admin':
        data = Books(
            title=request.form['title'],
            year=request.form['year'],
            total_pages=request.form['total_pages'],
            id_category=request.form['id_category']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Book created successfully'}, 201
    else:
        return {'message': 'Access denied'}, 403

@app.route('/books/<int:id_book>', methods=['PUT'])
@login_required
def update_book(id_book):
    if current_user.user_type == 'admin':
        data = Books.query.get(id_book)
        if data:
            data.title = request.form['title']
            data.year = request.form['year']
            data.total_pages = request.form['total_pages']
            data.id_category = request.form['id_category']
            db.session.commit()
            return {'message': 'Book updated successfully'}
        else:
            return {'message': 'Book not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/books/<int:id_book>', methods=['DELETE'])
@login_required
def delete_book(id_book):
    if current_user.user_type == 'admin':
        data = Books.query.get(id_book)
        if data:
            db.session.delete(data)
            db.session.commit()
            return {'message': 'Book deleted successfully'}
        else:
            return {'message': 'Book not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/authors', methods=['GET'])
@login_required
def view_authors():
    data = Authors.query.order_by(Authors.id_author.desc()).all()
    authors_list = []
    for el in data:
        authors_list.append({
            'id_author': el.id_author,
            'name': el.name,
            'nationality': el.nationality,
            'year_birth': el.year_birth
        })
    return {'authors': authors_list}

@app.route('/authors', methods=['POST'])
@login_required
def create_author():
    if current_user.user_type == 'admin':
        data = Authors(
            name=request.form['name'],
            nationality=request.form['nationality'],
            year_birth=request.form['year_birth']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Author created successfully'}, 201
    else:
        return {'message': 'Access denied'}, 403

@app.route('/authors/<int:id_author>', methods=['PUT'])
@login_required
def update_author(id_author):
    if current_user.user_type == 'admin':
        data = Authors.query.get(id_author)
        if data:
            data.name = request.form['name']
            data.nationality = request.form['nationality']
            data.year_birth = request.form['year_birth']
            db.session.commit()
            return {'message': 'Author updated successfully'}
        else:
            return {'message': 'Author not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/authors/<int:id_author>', methods=['DELETE'])
@login_required
def delete_author(id_author):
    if current_user.user_type == 'admin':
        data = Authors.query.get(id_author)
        if data:
            db.session.delete(data)
            db.session.commit()
            return {'message': 'Author deleted successfully'}
        else:
            return {'message': 'Author not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/book_authors', methods=['GET'])
@login_required
def view_book_authors():
    data = BookAuthors.query.order_by(BookAuthors.id_book_author.desc()).all()
    book_authors_list = []
    for el in data:
        book_authors_list.append({
            'id_book_author': el.id_book_author,
            'id_book': el.id_book,
            'id_author': el.id_author,
            'book': {
                'title': el.book.title,
                'year': el.book.year,
                'total_pages': el.book.total_pages,
                'id_category': el.book.id_category,
                'category': {
                    'name': el.book.category.name,
                    'description': el.book.category.description
                }
            },
            'author': {
                'name': el.author.name,
                'nationality': el.author.nationality
            }
        })
    return {'book_authors': book_authors_list}

@app.route('/book_authors', methods=['POST'])
@login_required
def create_book_author():
    if current_user.user_type == 'admin':
        data = BookAuthors(
            id_book=request.form['id_book'],
            id_author=request.form['id_author']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Book author created successfully'}, 201
    else:
        return {'message': 'Access denied'}, 403

@app.route('/book_authors/<int:id_book_author>', methods=['PUT'])
@login_required
def update_book_author(id_book_author):
    if current_user.user_type == 'admin':
        data = BookAuthors.query.get(id_book_author)
        if data:
            data.id_book = request.form['id_book']
            data.id_author = request.form['id_author']
            db.session.commit()
            return {'message': 'Book author updated successfully'}
        else:
            return {'message': 'Book author not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/book_authors/<int:id_book_author>', methods=['DELETE'])
@login_required
def delete_book_author(id_book_author):
    if current_user.user_type == 'admin':
        data = BookAuthors.query.get(id_book_author)
        if data:
            db.session.delete(data)
            db.session.commit()
            return {'message': 'Book author deleted successfully'}
        else:
            return {'message': 'Book author not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/users', methods=['GET'])
@login_required
def view_users():
    if current_user.user_type == 'admin':
        data = Users.query.order_by(Users.id_user.desc()).all()
        users_list = []
        for el in data:
            users_list.append({
                'id_user': el.id_user,
                'username': el.username,
                'user_type': el.user_type
            })
        return {'users': users_list}
    else:
        return {'message': 'Access denied'}

@app.route('/users', methods=['POST'])
@login_required
def create_user():
    if current_user.user_type == 'admin':
        user = Users(
            username=request.form['username'],
            password=request.form['password'],
            user_type=request.form['user_type']
        )
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201
    else:
        return {'message': 'Access denied'}, 403

@app.route('/user_members', methods=['POST'])
@login_required
def create_user_member():
    user = Users(
        username=request.form['username'],
        password=request.form['password'],
        user_type='member'
    )
    db.session.add(user)
    db.session.commit()
    return {'message': 'User created successfully'}, 201

@app.route('/users/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    if current_user.user_type == 'admin':
        data = Users.query.get(id_user)
        if data:
            data.username = request.form['username']
            data.user_type = request.form['user_type']
            db.session.commit()
            return {'message': 'User updated successfully'}
        else:
            return {'message': 'User not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/users/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    if current_user.user_type == 'admin':
        data = Users.query.get(id_user)
        if data:
            db.session.delete(data)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        else:
            return {'message': 'User not found'}, 404
    else:
        return {'message': 'Access denied'}, 403

@app.route('/transactions', methods=['GET'])
@login_required
def view_transactions():
    if current_user.user_type == 'admin':
        data = Transactions.query.order_by(Transactions.id_transaction.desc()).all()
        transactions_list = []
        for el in data:
            transactions_list.append({
                'id_transaction': el.id_transaction,
                'id_admin': el.id_admin,
                'id_member': el.id_member,
                'borrowing_date': el.borrowing_date,
                'users': {
                    'member': el.member.username,
                    'admin': el.admin.username
                }
            })
        return {'transactions': transactions_list}
    else:
        return {'message': 'Access denied'}

@app.route('/transactions/add', methods=['POST'])
@login_required
def create_transaction():
    if current_user.user_type == 'admin':
        data = request.json
        
        transaction = Transactions(
            id_admin=data['id_admin'],
            id_member=data['id_member'],
            borrowing_date=data['borrowing_date']
        )
        db.session.add(transaction)
        db.session.commit()
        
        for detail in data['transaction_details']:
            transaction_detail = TransactionDetails(
                id_transaction=transaction.id_transaction,
                id_book=detail['id_book'],
                return_date=detail['return_date']
            )
            db.session.add(transaction_detail)
        db.session.commit()
        
        return {'message': 'Transaction created successfully'}, 201
    else:
        return {'message': 'Access denied'}

@app.route('/transaction_details', methods=['GET'])
@login_required
def view_transaction_details():
    if current_user.user_type == 'admin':
        data = TransactionDetails.query.order_by(TransactionDetails.id_transaction_detail.desc()).all()
        transaction_details_list = []
        for el in data:
            transaction_details_list.append({
                'id_transaction_detail': el.id_transaction_detail,
                'id_transaction': el.id_transaction,
                'id_book': el.id_book,
                'return_date': el.return_date,
                'transaction': {
                    'id_admin': el.transaction.id_admin,
                    'id_member': el.transaction.id_member,
                    'borrowing_date': el.transaction.borrowing_date,
                    'users': {
                        'member': el.transaction.member.username,
                        'admin': el.transaction.admin.username
                    }
                },
                'book': {
                    'title': el.book.title
                }
            })
        return {'transaction_details': transaction_details_list}
    else:
        return {'message': 'Access denied'}

if __name__ == '__main__':
    app.run(debug=True)