from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    
    # Configure SQLite database
    basedir = path.abspath(path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(path.dirname(basedir), "instance", DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        basedir = path.abspath(path.dirname(__file__))
        instance_path = path.join(path.dirname(basedir), 'instance')
        
        # Create instance directory if it doesn't exist
        if not path.exists(instance_path):
            import os
            os.makedirs(instance_path, exist_ok=True)
            os.chmod(instance_path, 0o777)
            print('Created Instance Directory!')
        
        # Check if database file exists
        db_file = path.join(instance_path, 'database.db')
        if not path.exists(db_file):
            db.create_all()
            print('Created SQLite Database!')
        else:
            print('Database already exists.')
