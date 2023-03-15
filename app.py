from flask import Flask
from flask_restful import Api
from src.resource import *
app = Flask(__name__)
api = Api(app)

DEBUG = True
HOST = "127.0.0.1" if DEBUG else "0.0.0.0"

api.add_resource(Popular, '/popular/<int:amount>')
api.add_resource(PopularList, '/popular')
api.add_resource(SameGenres, '/samegenres/<movie_name>')


# @app.route('/')
# def home():
#     return render_template('index.html')
#
#
# @app.route('/popular')
# @app.route('/popular/<int:amount>')
# def popular_movies(amount: int = 10):
#     result = get_popular_movies(amount)
#
#     if result['found'] is False:
#         return render_template('populate.html', result=result['response'].json(),
#                                status_code=result['response'].status_code)
#
#     return render_template('populate.html', result=result['response'], status_code=200)
#
#
# @app.route('/movie/<int:movie_id>/')
# @app.route('/movie/<int:movie_id>/<info_type>')
# def movie_info(movie_id: int, info_type: str = None):
#     info = get_movie_info(movie_id)
#
#     if info_type is None:
#         if info['found'] is False:
#             return render_template('movie_info.html', result=info['response'].json(),
#                                    status_code=info['response'].status_code, category="")
#
#         return render_template('movie_info.html', result=info['response'], status_code=200, category="")
#
#     elif info_type == "genres/equal":
#         pass
#     elif info_type == "runtime/similar":
#         pass
#     elif info_type == "actors/overlapping":
#         pass
#
#     return redirect(url_for("movie_info", movie_id=movie_id))
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(HOST, debug=DEBUG)
