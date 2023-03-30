from flask_restful import Resource, abort
from src.request_functions import *
from flask import request


class Movies(Resource):

    @staticmethod
    def get(movie_id: int):

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        return requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}').json()

    @staticmethod
    def delete(movie_id: int):

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        db.add_deleted(movie_id)

        return f"The movie with movie id {movie_id}, is successfully deleted.", 200

    @staticmethod
    def put(movie_id: int):

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        elif db.movie_is_liked(movie_id):
            db.unlike_movie(movie_id)

            return f"The movie with movie id {movie_id}, is successfully unliked.", 200

        db.like_movie(movie_id)

        return f"The movie with movie id {movie_id}, is successfully liked.", 200


class MoviesLists(Resource):

    @staticmethod
    def get():
        result = get_movies()

        if result['found'] is False:
            abort(404, message=result['response'])

        return result['response'], 200

    @staticmethod
    def delete():
        db.delete_all()
        return "All movies are successfully deleted.", 200

    @staticmethod
    def put():
        db.like_all()
        return "All movies are successfully liked.", 200


class Popular(Resource):

    @staticmethod
    def get():
        args = request.args
        amount = int(args['amount']) if 'amount' in args else 20

        result = get_popular_movies(amount)

        if result['found'] is False:
            abort(404, message=result['response'])

        return result['response'], 200


class SameGenres(Resource):

    @staticmethod
    def get(movie_id: int):

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        movie_genres: list[int] = get_movie_genres(movie_id)

        if movie_genres is None:
            abort(404, message=f'The movie with movie id {movie_id}, doesn\'t have genres.')

        matching_movies = get_matching_movies_genre(movie_genres)

        if matching_movies is None:
            abort(404,
                  message=f'A error occurred when searching matching movies for the movie with movie id {movie_id}')

        return matching_movies, 200


class SimilarRuntime(Resource):

    @staticmethod
    def get(movie_id):

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        runtime: int = get_runtime_movie(movie_id)

        if runtime is None:
            abort(404, message=f'A error occurred when requesting the runtime of the movie with movie id {movie_id}')

        similar_runtime = get_similar_runtime_movies(runtime)

        if similar_runtime is None:
            abort(404,
                  message=f'A error occurred when searching movies with a similar runtime as the movie with movie id {movie_id}')

        return similar_runtime, 200


class OverlappingActors(Resource):

    @staticmethod
    def get(movie_id: int):

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        cast = get_cast_movie(movie_id)

        if cast is None:
            abort(404, message=f'A error occurred when requesting the cast of the movie with movie id {movie_id}')

        overlapping_actors = get_overlapping_actors(cast)

        if overlapping_actors is None:
            abort(404,
                  message=f'A error occurred when searching movies with overlapping actors as the movie with movie id {movie_id}')

        return overlapping_actors, 200


class CompareMovies(Resource):

    @staticmethod
    def get():

        args = request.args

        average_scores = []
        movie_names = []

        if 'movies' in args:
            movies_listed = []
            movies_listed.extend(args['movies'].split(','))

            for movie_id in movies_listed:

                if not movie_exists(int(movie_id)):
                    abort(404, message=f'The movie id: {movie_id} is not valid.')

                movie_name: str = get_movie_name(int(movie_id))

                if movie_name is None:
                    abort(404,
                          message=f'A error occurred when requesting the movie name for the movie with movie id {movie_id}.')

                vote_avg: float = get_average_vote(int(movie_id))

                if vote_avg is None:
                    abort(404, message=f'A error occurred when requesting the vote average for the movie with movie id {movie_id}.')

                average_scores.append(vote_avg)
                movie_names.append(movie_name)

        chart_data = {'type': 'bar', "data": {}}
        chart_data["data"]["labels"] = movie_names
        datasets = {"label": "Voting average", "data": average_scores}
        chart_data["data"]["datasets"] = [datasets]

        return chart_data, 200
