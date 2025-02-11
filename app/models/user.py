from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import avinit
from sqlalchemy import text


current_year = datetime.now().year
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(512))
    lastname = db.Column(db.String(512))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    
    
    def __repr__(self) -> str:
        return 'User>>> {self.username}'
    
    def generate_pass(self, password):
        self.password = generate_password_hash(password)
        
    def check_pass(self, password:str):
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
     
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def emailExists(cls, email):
        return cls.query.filter_by(email=email).first() is not None
    
    @classmethod
    def usernameExists(cls, username):
        return cls.query.filter_by(username=username).first() is not None
    
    @classmethod
    def insert_user(cls, username, firstname, lastname, password):
        query = text("""
            INSERT INTO user (username, firstname, lastname, password) 
            VALUES (:username, :firstname, :lastname, :password)
        """)
        result = db.session.execute(query, {
            'username': username,
            'firstname': firstname,
            'lastname': lastname,
            'password': password
        })
        db.session.commit()
        return result
    
    @classmethod
    def usernameExistsSQL(cls, username):
        query = text("SELECT 1 FROM user WHERE username = :username LIMIT 1")
        result = db.session.execute(query, {'username': username}).fetchone()
        return result is not None
    
    @property
    def profile_picture(self):
        first_initial = self.firstname[0] if self.firstname else ""
        last_initial = self.lastname[0] if self.lastname else ""
        intials= f"{first_initial} {last_initial}".upper()
        profile = avinit.get_avatar_data_url(intials)
        return profile
    
    @property
    def profile_picture(self):
        first_initial = self.firstname[0] if self.firstname else ""
        last_initial = self.lastname[0] if self.lastname else ""
        intials= f"{first_initial} {last_initial}".upper()
        profile = avinit.get_avatar_data_url(intials)
        return profile
    
    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}".strip()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
