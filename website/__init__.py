from flask import Flask
from flask_login import LoginManager, login_user


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'laksumi somaskanthamoorthy'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .views import views
    from .auth import auth
    from .models import db, User
    from .encryted_download import encrypt_file
    db.init_app(app)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Assuming your User model and db are imported correctly at the top or within this function
        return User.query.get(int(user_id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(encrypt_file, url_prefix='/')
    return app
