from app.extensions import db
from sqlalchemy import desc
from uuid import uuid4
from datetime import datetime

from app.models.user import User

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid4()))
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #Foreign key to User table
    movie_id = db.Column(db.String(), db.ForeignKey('movie.id'), nullable=False) #Foreign key to Movie table
    created_at = db.Column(db.DateTime(), default=datetime.now)
    user = db.relationship('User', backref='reviews')
    def to_dict(self):
        return {
            'id': self.id,
            'title':self.title,
            'rating': self.rating,
            'comment': self.comment,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'created_at': self.created_at.strftime("%d %B %Y %I:%M %p")
        }
        
    def to_dict_with_user(self):
        review_data = self.to_dict()
        user: User = User.query.get(self.user_id)
        if user:
            review_data['user'] = { 
                'id': user.id,
                'username': user.username,
                'profile_picture': user.profile_picture,
                'full_name': user.full_name
            }
        return review_data
    
    @classmethod
    def getReviews(cls, movieId:str, user_id):
        reviews_query = None
        if user_id is not None:
            reviews_query = cls.query.filter(cls.movie_id == movieId, cls.user_id != user_id)
        else:
            reviews_query = cls.query.filter(cls.movie_id == movieId)
        query = reviews_query.join(User).order_by(cls.created_at.desc())
        
        return query
    
    @classmethod
    def getUserReviews(cls, movieId:str, user_id):
        reviews_query = cls.query.filter_by(movie_id=movieId, user_id=user_id)
        query = reviews_query.join(User).order_by(cls.created_at.desc())
        
        return query
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
