from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from datetime import datetime
from sqlalchemy import func, and_
from sqlalchemy import desc
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import text
from app.models.review import Review
from app.reviewschema import ReviewSchema
from app.movieschema import MovieSchema, calculate_movie_data, calculate_movies_data
from app.models.movie import Movie

movies = Blueprint("movies", __name__)



@movies.get('/')
def get_featured_movies():
    
    user_id = current_user.id if current_user.is_authenticated else None
    db_movies = Movie.get_featured_movies2(user_id)
    top_movie = db_movies[0] if db_movies else None
    return render_template('movies.html', movies=db_movies, top_movie=top_movie)


@movies.get('/top-rated')
def get_top_rate():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=25, type=int)
    search_query = request.args.get('search', default='', type=str) 
    
    top_rated_movies_query = Movie.get_top_rated()
    
    if search_query:
        top_rated_movies_query = top_rated_movies_query.filter(Movie.title.ilike(f'%{search_query}%'))  # Example: search by title
    

    top_rated_movies = top_rated_movies_query.paginate(page=page, per_page=per_page, error_out=False)

    res = calculate_movies_data(top_rated_movies.items)

    return render_template('top-rated-movies.html',
        movies=res,
        page=top_rated_movies.page,
        per_page=top_rated_movies.per_page,
        total_pages=top_rated_movies.pages,
        total_items=top_rated_movies.total,
        search_query=search_query,
        next_page="/top-rated"
    )

@movies.get('/released')
def get_new_released():
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=25, type=int)
    search_query = request.args.get('search', default='', type=str) 
    
    get_new_released = Movie.get_new_released()
    
    if search_query:
        get_new_released = get_new_released.filter(Movie.title.ilike(f'%{search_query}%'))  # Example: search by title
    

    top_rated_movies = get_new_released.paginate(page=page, per_page=per_page, error_out=False)

    res = calculate_movies_data(top_rated_movies.items)

    return render_template('top-rated-movies.html',
        movies=res,
        page=top_rated_movies.page,
        per_page=top_rated_movies.per_page,
        total_pages=top_rated_movies.pages,
        total_items=top_rated_movies.total,
        search_query=search_query,
        next_page="/top-rated"
    )

@movies.get('/all-movies')
def get_all_movies():
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=25, type=int)
    search_query = request.args.get('search', default='', type=str) 
    
    if search_query:
        all_movies = Movie.query.filter(Movie.title.ilike(f'%{search_query}%')).paginate(page=page, per_page=per_page, error_out=False)
    else :
        all_movies = Movie.query.paginate(page=page, per_page=per_page, error_out=False)


    res = calculate_movies_data(all_movies.items)

    return render_template('all-movies.html',
        movies=res,
        page=all_movies.page,
        per_page=all_movies.per_page,
        total_pages=all_movies.pages,
        total_items=all_movies.total,
        search_query=search_query
    )   
    
@movies.get('/movies/<id>',  endpoint='get_movie')
def get_movie(id):
    
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    db_movie:Movie = Movie.query.get(id)
    movie = calculate_movie_data(db_movie)
    user_id = current_user.id if current_user.is_authenticated else None
    my_reviews = None
    movie_reviews =None
    
    if user_id:
        user_review = Review.getUserReviews(movieId=db_movie.id, user_id=user_id).first()
        my_reviews = ReviewSchema().dump(user_review) if user_review else None
        movie_reviews = Review.getReviews(movieId=db_movie.id, user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    else:
        movie_reviews = Review.getReviews(movieId=db_movie.id,  user_id=None).paginate(page=page, per_page=per_page, error_out=False)

    
    reviews_data = ReviewSchema(many=True).dump(movie_reviews.items)

    return render_template('movie.html', 
                           movie=movie,
                           reviews=reviews_data,
                           page=movie_reviews.page,
                           user_reviews=my_reviews,
                           per_page=movie_reviews.per_page,
                           total_pages=movie_reviews.pages,
                           total_items=movie_reviews.total)


 


@movies.route('/movies/<id>/reviews', methods=['GET', 'POST'])
@login_required
def get_movie_with_reviews(id):
    user_id = current_user.id if current_user.is_authenticated else None
    if request.method == 'POST':
        title = request.form.get('title')
        comment = request.form.get('reviewComment')
        rating = request.form.get('rating')
        movie_id = id
        review = Review(title=title, comment=comment, rating=rating, user_id=user_id, movie_id=movie_id)
        review.save()
    
        return redirect(url_for('movies.get_movie', id=id))
    
    db_movie:Movie = Movie.query.get(id)
    movie = calculate_movie_data(db_movie)
    return render_template('movie-reviews.html', movie=movie)        


@movies.get('/check_review/<id>')
@login_required
def check_review(id):
    user_id = current_user.id if current_user.is_authenticated else None
    review = Review.getUserReviews(movieId=id, user_id=user_id).first()
    if review is not None:
        flash("You've already submitted a review for this movie!", category='info')
        return {'exists': True} 
    return {'exists': False} 