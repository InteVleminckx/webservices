from flask import Flask
from flask_restful import Api
from src.resource import *

app = Flask(__name__)
api = Api(app)

DEBUG = True
HOST = "127.0.0.1" if DEBUG else "0.0.0.0"

api.add_resource(Movies, '/movies/<movie_name>')
api.add_resource(MoviesLists, '/', '/movies/', '/movies/same-genres', '/movies/similar-runtime',
                 '/movies/overlapping-actors')
api.add_resource(Popular, '/movies/popular/<int:amount>')
api.add_resource(PopularList, '/movies/popular')
api.add_resource(SameGenres, '/movies/same-genres/<movie_name>')
api.add_resource(SimilarRuntime, '/movies/similar-runtime/<movie_name>')
api.add_resource(OverlappingActors, '/movies/overlapping-actors/<movie_name>')
api.add_resource(CompareMovies, '/movies/compare/<movies>')

if __name__ == "__main__":
    app.run(HOST, debug=DEBUG)
