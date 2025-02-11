from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, post_dump
from app.models.movie import Movie 
from flask_login import current_user
from marshmallow import  fields
import marshmallow_sqlalchemy as ma


def calculate_movie_data(movie:Movie, include_rates:bool = True, include_reviews:bool = True):

    movie_data = {
        'id': movie.id,
        'title': movie.title,
        'year': int(movie.year),
        'runtime':movie.runtime,
        'director':movie.director,
        'writer':movie.writer,
        'plot': movie.plot,
        'actors': movie.actors,
        'language': movie.language,
        'country': movie.country,
        'awards': movie.awards,
        'movie_genres' : [genre.strip() for genre in movie.genre.split(",")],
        'poster': movie.poster,
        'trailer':movie.trailer
    }
    
    ratings = [r.rating for r in movie.reviews if r.rating is not None]
    movie_data['average_rating'] = round(sum(ratings) / len(ratings), 2) if ratings else 0
    
    if current_user.is_authenticated:
        user_ratings = [r.rating for r in movie.reviews if r.rating is not None and r.user_id == current_user.id]
        movie_data['user_rating'] = round(sum(user_ratings) / len(user_ratings), 2) if user_ratings else 0
    else:
        movie_data['user_rating'] = 0

    return movie_data

def calculate_movies_data(movies, include_rates:bool = True, include_reviews:bool = True):
    movies_data = []
    for movie in movies:
        movie_data = calculate_movie_data(movie=movie, include_rates=include_rates, include_reviews=include_reviews)
        movies_data.append(movie_data)
    return movies_data
         
class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True
        include_fk = True

    reviews = fields.Nested('ReviewSchema', many=True)
    
    @post_dump
    def add_extra_data(self, data, **kwargs):
        include_ratings = kwargs.get('include_ratings', True)  # Default to True
        include_reviews = kwargs.get('include_reviews', True)
        
        
        movie: Movie = Movie.query.get(data['id'])
        if movie:
            reviews_query = movie.reviews  # This is the dynamic query
            paginated_reviews = reviews_query(page=1, per_page=2)
            print("Pagniated", paginated_reviews.items)
            if include_ratings:
                ratings = [r.rating for r in movie.reviews if r.rating is not None]
                data['average_rating'] = round(sum(ratings) / len(ratings), 2) if ratings else 0
                
                if current_user is not None:
                    user_ratings = [r.rating for r in movie.reviews if r.rating is not None and r.user_id == current_user.id]
                    data['user_rating'] = round(sum(user_ratings) / len(user_ratings), 2) if user_ratings else 0
                else:
                    data['user_rating'] = 0
            if include_reviews:
                data['reviews'] = [
                    review.to_dict_with_user()
                    for review in movie.reviews
                ]
        return data

    