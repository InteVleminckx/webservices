from flask import Flask
from flask.templating import render_template
from src.popular_movies import *

app = Flask(__name__)

DEBUG = True
HOST = "127.0.0.1" if DEBUG else "0.0.0.0"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/popular')
def all_popular_movies():
    return get_popular_movies()


@app.route('/popular/<int:x>')
def popular_movies(x):
    result = get_popular_movies(x)

    if result[0] is False:
        return render_template('populate.html', result=result[1].json(), status_code=result[1].status_code)

    return render_template('populate.html', result=result[1], status_code=200)


if __name__ == "__main__":
    app.run(HOST, debug=DEBUG)
