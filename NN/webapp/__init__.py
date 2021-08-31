from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

"""app initialisation module"""

#create sqlaclhemy object
db = SQLAlchemy()

#app factory
def create_app():
    #create app
    app = Flask(__name__)
    #configure app
    app.config['SECRET_KEY'] = 'Kirill'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    #configure login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    #route for user loader.
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    #register app to db
    db.init_app(app)

    #load blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
