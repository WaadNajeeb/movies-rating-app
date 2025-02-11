from app.extensions import db
from sqlalchemy import func
from sqlalchemy import desc
from uuid import uuid4
from app.models.review import Review
from datetime import datetime
from sqlalchemy import text

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(512), nullable=False, unique=True)
    year = db.Column(db.Integer)
    runtime = db.Column(db.String(255))
    director =db.Column(db.String(255))
    released = db.Column(db.String(512))
    writer = db.Column(db.String(512))
    actors = db.Column(db.String(512))
    genre = db.Column(db.String(255))
    plot = db.Column(db.Text)
    language = db.Column(db.String(128))
    country = db.Column(db.String(128))
    poster = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    awards = db.Column(db.String(255))
    reviews = db.relationship('Review', backref='movie', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> int:
        return f'Movie>>> {self.id}'
    

    @classmethod
    def get_features_movies(cls):
        s = (db.session.query(Movie, func.count(Review.id).label('reviews_count'))
             .join(Review, Review.movie_id == Movie.id)
             .group_by(Movie.id)
             .order_by(desc('reviews_count'))
             .limit(12)
             .all()
        )
        movies = [movie for movie, _ in s]  # List of Movie objects
        return movies
    
    @classmethod
    def get_featured_movies2(cls, user_id):
        sql_query = text("""
                SELECT 
                    m.*, 
                    ROUND(AVG(r.rating), 2) AS avg_rating, 
                    COALESCE(
                        (SELECT rating FROM review WHERE movie_id = m.id AND (user_id = :user_id OR :user_id IS NULL) LIMIT 1), 
                        0
                    ) AS user_rating
                FROM movie m
                JOIN review r ON r.movie_id = m.id
                GROUP BY m.id
                ORDER BY COUNT(r.id) DESC
                LIMIT 12;
            """)
        result = db.session.execute(sql_query, {"user_id": user_id})
        return result.fetchall()
    @classmethod
    def get_top_rated(cls):
       top_rated_movies_query = (cls.query.outerjoin(Review)
                                .group_by(Movie.id)
                                .having(func.avg(Review.rating) > 7)  # Filter movies with avg rating > 7
                                .order_by(func.avg(Review.rating).desc()))
    
       return top_rated_movies_query
    
    @classmethod
    def get_new_released(cls):
        
        newly_released = (cls.query
                .filter(Movie.year.between(2000, datetime.now().year))
                .order_by(Movie.year.asc())) 
    
        return newly_released