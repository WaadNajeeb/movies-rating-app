import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.models.user import User
from app.routes import auth_routes, movie_route 

# Load environment variables from .env file
load_dotenv()

db:SQLAlchemy = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    # Disable Flask-SQLAlchemy track modifications (optional)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

     # Initialize LoginManager with the app
    login_manager.init_app(app)

    # Set the login view (route where users should be redirected to login)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    # Register blueprints (import your routes here)
    app.register_blueprint(auth_routes.auth, url_prefix='/auth')
    app.register_blueprint(movie_route.movies, url_prefix='/')

    return app
