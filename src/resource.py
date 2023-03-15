from flask_restful import Resource, abort
from src.request_functions import *


class Popular(Resource):

    def get(self, amount: int):
        result = get_popular_movies(amount)

        if result['found'] is False:
            abort(404, message=result['response'])

        return result['response'], 200


class PopularList(Resource):

    def get(self):
        result = get_popular_movies(10)

        if result['found'] is False:
            abort(404, message=result['response'])

        return result['response'], 200


class SameGenres(Resource):

    def get(self, movie_name: str):
        movie_id: int = get_movie_id(movie_name)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} is not vallid.')

        movie_genres: list[int] = get_movie_genres(movie_id)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} doesn\'t have genres.')

        matching_movies = get_matching_movies_genre(movie_genres)

        if matching_movies is None:
            abort(404, message=f'A error occured when searching matching movies for {movie_name}')

        return matching_movies, 200
