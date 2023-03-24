from flask import Flask, render_template
from flask_restful import Api
from src.resource import *

app = Flask(__name__)
api = Api(app)

DEBUG = True
HOST = "127.0.0.1" if DEBUG else "0.0.0.0"

api.add_resource(Movies, '/movies/<movie_name>')
api.add_resource(MoviesLists, '/', '/movies/')
api.add_resource(Popular, '/movies/popular/<int:amount>')
api.add_resource(PopularList, '/movies/popular')
api.add_resource(SameGenres, '/movies/<movie_name>/same-genres')
api.add_resource(SimilarRuntime, '/movies/<movie_name>/similar-runtime')
api.add_resource(OverlappingActors, '/movies/<movie_name>/overlapping-actors')
api.add_resource(CompareMovies, '/movies/compare/<movies>')


# Nog eens navragen
@app.route('/website')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(HOST, debug=DEBUG)
