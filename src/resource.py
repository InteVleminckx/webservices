from flask_restful import Resource, abort
from src.request_functions import *


class Movies(Resource):

    @staticmethod
    def get(movie_name: str):
        movie_id: int = get_movie_id(movie_name)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} is not valid.')

        return requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}').json()

    @staticmethod
    def delete(movie_name: str):
        movie_id: int = get_movie_id(movie_name)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} is not valid.')

        db.add_deleted(movie_id)

        return f"{movie_name} is successfully deleted.", 200

    @staticmethod
    def put(movie_name: str):
        movie_id: int = get_movie_id(movie_name)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} is not valid.')

        elif db.movie_is_liked(movie_id):
            db.unlike_movie(movie_id)

            return f"{movie_name} is successfully unliked.", 200

        db.like_movie(movie_id)

        return f"{movie_name} is successfully liked.", 200


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
    def get(amount: int):
        result = get_popular_movies(amount)

        if result['found'] is False:
            abort(404, message=result['response'])

        return result['response'], 200


class PopularList(Resource):

    @staticmethod
    def get():
        result = get_popular_movies(10)

        if result['found'] is False:
            abort(404, message=result['response'])

        return result['response'], 200


class SameGenres(Resource):

    @staticmethod
    def get(movie_name: str):
        movie_id: int = get_movie_id(movie_name)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} is not valid.')

        movie_genres: list[int] = get_movie_genres(movie_id)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} doesn\'t have genres.')

        matching_movies = get_matching_movies_genre(movie_genres)

        if matching_movies is None:
            abort(404, message=f'A error occurred when searching matching movies for {movie_name}')

        return matching_movies, 200


class SimilarRuntime(Resource):

    @staticmethod
    def get(movie_name: str):
        movie_id: int = get_movie_id(movie_name)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} is not valid.')

        runtime: int = get_runtime_movie(movie_id)

        if runtime is None:
            abort(404, message=f'A error occurred when requesting the runtime of the movie: {movie_name}')

        similar_runtime = get_similar_runtime_movies(runtime)

        if similar_runtime is None:
            abort(404, message=f'A error occurred when searching movies with a similar runtime as {movie_name}')

        return similar_runtime, 200


class OverlappingActors(Resource):

    @staticmethod
    def get(movie_name: str):
        movie_id: int = get_movie_id(movie_name)

        if movie_id is None:
            abort(404, message=f'The movie: {movie_name} is not valid.')

        cast = get_cast_movie(movie_id)

        if cast is None:
            abort(404, message=f'A error occurred when requesting the cast of the movie: {movie_name}')

        overlapping_actors = get_overlapping_actors(cast)

        if overlapping_actors is None:
            abort(404, message=f'A error occurred when searching movies with overlapping actors as {movie_name}')

        return overlapping_actors, 200


class CompareMovies(Resource):

    @staticmethod
    def get(movies: str):
        movies_listed = []
        movies_listed.extend(movies.split(','))

        average_scores = []

        for movie in movies_listed:

            movie_id: int = get_movie_id(movie)

            if movie_id is None:
                abort(404, message=f'The movie: {movie} is not valid.')

            vote_avg: float = get_average_vote(movie_id)

            if vote_avg is None:
                abort(404, message=f'A error occurred when requesting the vote average for: {movie}.')

            average_scores.append(vote_avg)

        chart_data = {'type': 'bar', "data": {}}
        chart_data["data"]["labels"] = movies_listed
        datasets = {"label": "Voting average", "data": average_scores}
        chart_data["data"]["datasets"] = [datasets]

        return chart_data, 200
