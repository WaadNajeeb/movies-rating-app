import os
from flask import Flask, render_template
from flask_login import LoginManager
from app.extensions import db
from dotenv import load_dotenv
from app.models.user import User
from app.routes import auth_routes, movie_route 
from app.config.config import config_by_name
from flask_wtf.csrf import CSRFProtect

# Load environment variables from .env file
load_dotenv()
login_manager = LoginManager()

def create_app(config_name="development"):
    app = Flask(__name__)
    csrf = CSRFProtect(app)

    app.config.from_object(config_by_name[config_name])

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

    @app.route("/")
    def get_home():
        return render_template('movies.html')
    return app
