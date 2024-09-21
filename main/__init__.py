from flask import Flask
from flask_login import LoginManager, UserMixin

from . import config as cnf
from .database import db

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(cnf.Config)

    db.init_app(app)

    with app.app_context():
        from .models import User
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'login'


    @login_manager.user_loader
    def user_loader(user_id):
        from .models import User
        return User.query.get(user_id)


    from .routes.auth import auth
    from .routes.main import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app

