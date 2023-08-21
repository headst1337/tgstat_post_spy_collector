from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from . config import Config


login_manager = LoginManager()
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from .scheduler import bp as scheduler_bp
    app.register_blueprint(scheduler_bp)

    with app.app_context():
        db.create_all()

    return app

from . models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))