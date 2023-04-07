import re

from flask_restful import Resource, abort
from src.request_functions import *
from flask import request


class Movies(Resource):

    @staticmethod
    def get(movie_id: int) -> tuple[dict, int]:
        """
        Retrieve a movie's information by its ID.

        Parameters
        ----------
            movie_id (int): The ID of the movie to retrieve.

        Returns
        -------
            A dictionary containing the following movie information:
                - id (int): The ID of the movie.
                - title (str): The original title of the movie.
                - liked (bool): Whether the movie is liked by the user or not.

            The status code:
                - 200 OK: The request was successful and the movie details are returned.
                - 404 Not Found: The movie ID provided is not valid.

        Raises
        ------
            HTTPException: If the movie ID is not valid.

        Example
        -------
            >>> 'GET http://127.0.0.1:5000/movies/10597'
            {
                "id": 10597,
                "title": "Kevin & Perry Go Large",
                "liked": false
            }

        """

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}').json()

        movie = {'id': response['id'], 'title': response['original_title']}
        movie['liked'] = db.movie_is_liked(movie['id'])

        return movie, 200

    @staticmethod
    def delete(movie_id: int) -> tuple[str, int]:
        """
        Delete a movie by its ID.

        Parameters
        ----------
            movie_id (int): The ID of the movie to delete.

        Returns
        -------
            A string message indicating that the movie with the given ID has been deleted successfully.

            The status code:
                - 200 OK: The request was successful and the movie was deleted.
                - 404 Not Found: The movie ID provided is not valid.

        Raises
        ------
            HTTPException: If the movie ID is not valid.

        Example
        -------
            >>> 'DELETE http://127.0.0.1:5000/movies/10597'
            "The movie with movie id 10597, is successfully deleted."
        """

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        db.add_deleted(movie_id)

        return f"The movie with movie id {movie_id}, is successfully deleted.", 200

    @staticmethod
    def put(movie_id: int) -> tuple[str, int]:
        """
        Like or unlike a movie by its ID.

        Parameters
        ----------
            movie_id (int): The ID of the movie to like or unlike.

        Returns
        -------
            A string message indicating whether the movie was successfully liked or unliked.

            The status code:
                - 200 OK: The request was successful.
                - 404 Not Found: The movie ID provided is not valid.

        Raises
        ------
            HTTPException: If the movie ID is not valid.

        Example
        -------
            >>> 'PUT http://127.0.0.1:5000/movies/10597'
            "The movie with movie id 10597, is successfully liked."

        """

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
        """
        Retrieve information over the first 20 movie's.

        Returns
        -------
            Returns a dictionary containing the information for the first 20 movies.
            Each movie's information is represented by a dictionary with the following keys:
                - id (int): The ID of the movie.
                - title (str): The original title of the movie.
                - liked (bool): Whether the movie is liked by the user or not.

            The status code:
                - 200 OK: The request was successful and the movie details are returned.
                - 404 Not Found: The movie ID provided is not valid.

        Raises
        ------
            HTTPException: If the movie ID is not valid.

        Example
        -------
            >>> 'GET http://127.0.0.1:5000/movies'
            {
                0: {
                    "id": 10597,
                    "title": "Kevin & Perry Go Large",
                    "liked": false
                },
                ...
                19: {
                    "id": 76600,
                    "title": "Avatar: The Way of Water",
                    "liked": false
                }
            }
        """

        result = get_movies()

        if result['found'] is False:
            abort(404, message=result['response'])

        return result['response'], 200

    @staticmethod
    def delete() -> tuple[str, int]:
        """
        Delete all movies.

        Returns
        -------
            A string containing the message:
            - "All movies are successfully deleted."

            The status code:
            - 200 OK: The request was successful.

        Example
        -------
            >>> 'DELETE http://127.0.0.1:5000/movies'
            "All movies are successfully deleted."

        """

        db.delete_all()
        return "All movies are successfully deleted.", 200

    @staticmethod
    def put() -> tuple[str, int]:
        """
        Like all movies.

        Returns
        -------
            A string containing the message:
            - "All movies are successfully liked."

            The status code:
            - 200 OK: The request was successful.

        Example
        -------
            >>> 'PUT http://127.0.0.1:5000/movies'
            "All movies are successfully liked."

        """

        db.like_all()
        return "All movies are successfully liked.", 200


class Popular(Resource):

    @staticmethod
    def get() -> tuple[dict, int]:
        """
        Retrieve information on popular movies.

        Arguments
        ----------
        amount : (int), optional
            The number of popular movies to retrieve. Default value is 20.

        Returns
        -------
        A dictionary containing the information for the popular movies.

        Each movie's information is represented by a dictionary with the following keys:
            - id (int): The ID of the movie.
            - title (str): The original title of the movie.
            - liked (bool): Whether the movie is liked by the user or not.

        The status code:
            - 200 OK: The request was successful and the movie details are returned.
            - 404 Not Found: The movies could not be found.

        Raises
        ------
        HTTPException: If the movie ID is not valid.

        Example
        -------
        >>> 'GET http://127.0.0.1:5000/movies/popular?amount=x'
        {
            0: {
                "id": 10597,
                "title": "Kevin & Perry Go Large",
                "liked": false
            },
            ...
            x: {
                "id": 76600,
                "title": "Avatar: The Way of Water",
                "liked": false
            }
        }
        """

        args = request.args

        amount = 20

        if 'amount' in args:
            if args['amount'] is not None:
                if args['amount'].isdigit():
                    amount = int(args['amount'])

        result = get_popular_movies(amount)

        if result['found'] is False:
            abort(404, message=result['response'])

        return result['response'], 200


class SameGenres(Resource):

    @staticmethod
    def get(movie_id: int):
        """
        Get information about movies with the same genre as the movie whose ID is given.

        Parameters
        ----------
        movie_id : (int): The ID of the movie to retrieve movies with the same genres.

        Returns
        -------
        A dictionary containing the information for the first 20 movies that have exactly the same genres.

        Each movie's information is represented by a dictionary with the following keys:
            - id (int): The ID of the movie.
            - title (str): The original title of the movie.
            - liked (bool): Whether the movie is liked by the user or not.

        The status code:
            - 200 OK: The request was successful and the movie details are returned.
            - 404 Not Found: The movies could not be found.

        Raises
        ------
        HTTPException:
            - If the movie ID is not valid.
            - If the movie doesn't have genres.
            - A error occurred when searching matching movies.

        Example
        -------
        >>> 'GET http://127.0.0.1:5000/movies/10597/same-genres'
        {
            0: {
                "id": 76600,
                "title": "Avatar: The Way of Water",
                "liked": false
            },
            ...
            19: {
                "id": 12345,
                "title": "Avatar",
                "liked": false
            }
        }
        """

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        movie_genres: list[int] = get_movie_genres(movie_id)

        if movie_genres is None:
            abort(404, message=f'The movie with movie id {movie_id}, doesn\'t have genres.')

        matching_movies = get_matching_movies_genre(movie_genres)

        if matching_movies is None:
            abort(404,
                  message=f'A error occurred when searching matching movies for '
                          f'the movie with movie id {movie_id}')

        return matching_movies, 200


class SimilarRuntime(Resource):

    @staticmethod
    def get(movie_id):
        """
        Get information about movies with the similar runtime as the movie whose ID is given.

        Parameters
        ----------
        movie_id : (int): The ID of the movie to retrieve movies with similar runtime.

        Returns
        -------
        A dictionary containing the information for the first 20 movies that have similar runtime (-10, +10) interval.

        Each movie's information is represented by a dictionary with the following keys:
            - id (int): The ID of the movie.
            - title (str): The original title of the movie.
            - liked (bool): Whether the movie is liked by the user or not.

        The status code:
            - 200 OK: The request was successful and the movie details are returned.
            - 404 Not Found: The movies could not be found.

        Raises
        ------
        HTTPException:
            - If the movie ID is not valid.
            - A error occurred when requesting the runtime of the movie.
            - A error occurred when searching matching movies.

        Example
        -------
        >>> 'GET http://127.0.0.1:5000/movies/10597/similar-runtime'
        {
            0: {
                "id": 76600,
                "title": "Avatar: The Way of Water",
                "liked": false
            },
            ...
            19: {
                "id": 12345,
                "title": "Avatar",
                "liked": false
            }
        }
        """

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        runtime: int = get_runtime_movie(movie_id)

        if runtime is None:
            abort(404, message=f'A error occurred when requesting the runtime of '
                               f'the movie with movie id {movie_id}')

        similar_runtime = get_similar_runtime_movies(runtime)

        if similar_runtime is None:
            abort(404,
                  message=f'A error occurred when searching movies with a similar runtime as '
                          f'the movie with movie id {movie_id}')

        return similar_runtime, 200


class OverlappingActors(Resource):

    @staticmethod
    def get(movie_id: int):
        """
        Get information about movies with 2 overlapping actors as the movie whose ID is given.

        Parameters
        ----------
        movie_id : (int): The ID of the movie to retrieve movies with overlapping actors.

        Returns
        -------
        A dictionary containing the information for the first 20 movies that have overlapping actors.

        Each movie's information is represented by a dictionary with the following keys:
            - id (int): The ID of the movie.
            - title (str): The original title of the movie.
            - liked (bool): Whether the movie is liked by the user or not.

        The status code:
            - 200 OK: The request was successful and the movie details are returned.
            - 404 Not Found: The movies could not be found.

        Raises
        ------
        HTTPException:
            - If the movie ID is not valid.
            - A error occurred when requesting the runtime of the movie.
            - A error occurred when searching matching movies.

        Example
        -------
        >>> 'GET http://127.0.0.1:5000/movies/10597/overlapping-actors'
        {
            0: {
                "id": 76600,
                "title": "Avatar: The Way of Water",
                "liked": false
            },
            ...
            19: {
                "id": 12345,
                "title": "Avatar",
                "liked": false
            }
        }
        """

        if not movie_exists(movie_id):
            abort(404, message=f'The movie id: {movie_id} is not valid.')

        cast = get_cast_movie(movie_id)

        if cast is None:
            abort(404, message=f'A error occurred when requesting the cast of '
                               f'the movie with movie id {movie_id}')

        overlapping_actors = get_overlapping_actors(cast)

        if overlapping_actors is None:
            abort(404,
                  message=f'A error occurred when searching movies with overlapping actors as '
                          f'the movie with movie id {movie_id}')

        return overlapping_actors, 200


class CompareMovies(Resource):

    @staticmethod
    def get():
        """
        Retrieve chart data for a list of movies.

        Arguments
        ---------
        movies : (str), optional
        A comma-separated string containing the IDs of the movies to retrieve chart data for.

        Returns
        -------
        A dictionary containing the chart data for the requested movies.

        The dictionary contains the following keys:
            - type (str): The type of chart being returned. Currently 'bar'.
            - data (dict): A dictionary containing the data for the chart.
            - labels (list of str): A list of the movie names for the requested movies.
            - datasets (list of dict): A list containing a single dictionary representing the dataset.
            - label (str): The label for the dataset. Currently set to 'Voting average'.
            - data (list of float): A list of the average voting scores for the requested movies.

        The status code:
            - 200 OK: The request was successful and the chart data is returned.
            - 404 Not Found: The movies or chart data could not be found.

        Raises
        ------
        HTTPException:
            - If the movie ID is not valid.
            - A error occurred when requesting the movie name.
            - A error occurred when requesting the vote average for a movie.

        Example
        -------
        >>> 'GET http://127.0.0.1:5000/movies/compare?movies=x,y,z'
        {
            "type": "bar",
                "data": {
                "labels": ["Movie X", "Movie Y", "Movie Z"],
                "datasets": [
                    {
                        "label": "Voting average",
                        "data": [7.5, 8.2, 6.7]
                    }
                ]
            }
        }
        """
        args = request.args

        average_scores = []
        movie_names = []

        if 'movies' in args:
            if args['movies'] is not None:
                pattern = "^[0-9,]+$"  # Met dit patroon kunnen we controleren dat onze string
                                       # enkel uit nummers en komma getallen bestaat

                if re.match(pattern, args['movies']):
                    movies_listed = []
                    movies_listed.extend(args['movies'].split(','))

                    for movie_id in movies_listed:

                        if not movie_exists(int(movie_id)):
                            abort(404, message=f'The movie id: {movie_id} is not valid.')

                        movie_name: str = get_movie_name(int(movie_id))

                        if movie_name is None:
                            abort(404,
                                  message=f'A error occurred when requesting the movie name for '
                                          f'the movie with movie id {movie_id}.')

                        vote_avg: float = get_average_vote(int(movie_id))

                        if vote_avg is None:
                            abort(404,
                                  message=f'A error occurred when requesting the vote average for '
                                          f'the movie with movie id {movie_id}.')

                        average_scores.append(vote_avg)
                        movie_names.append(movie_name)

        chart_data = {'type': 'bar', "data": {}}
        chart_data["data"]["labels"] = movie_names
        datasets = {"label": "Voting average", "data": average_scores}
        chart_data["data"]["datasets"] = [datasets]

        return chart_data, 200
