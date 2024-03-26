from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from app_library.models import app, db, Categories, Books, Users, Transactions, TransactionDetails

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
def view_categories():
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
        return {'message': 'Access denied'}

@app.route('/categories/add', methods=['POST'])
@login_required
def create_categories():
    if current_user.user_type == 'admin':
        data = Categories(
            name = request.form['name'],
            description = request.form['description']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Category created successfully'}
    else:
        return {'message': 'Access denied'}

@app.route('/categories/update', methods=['PUT'])
@login_required
def update_categories():
    if current_user.user_type == 'admin':
        data = Categories.query.get(request.form['id_category'])
        data.name = request.form['name']
        data.description = request.form['description']
        db.session.commit()
        return {'message': 'Category updated successfully'}
    else:
        return {'message': 'Access denied'}

@app.route('/categories/delete', methods=['DELETE'])
@login_required
def delete_categories():
    if current_user.user_type == 'admin':
        data = Categories.query.get(request.form['id_category'])
        db.session.delete(data)
        db.session.commit()
        return {'message': 'Category deleted successfully'}
    else:
        return {'message': 'Access denied'}

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
    return {'Books': books_list}

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
                'borrowing_date': el.borrowing_date
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
                'return_date': el.return_date
            })
        return {'transaction_details': transaction_details_list}
    else:
        return {'message': 'Access denied'}

if __name__ == '__main__':
    app.run(debug=True)
