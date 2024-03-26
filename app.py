from flask_login import LoginManager
from app_library.models import app
from app_library.routes import *

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)