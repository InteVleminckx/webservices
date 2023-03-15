from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

DEBUG = True
HOST = "127.0.0.1" if DEBUG else "0.0.0.0"

# API key: 48c964732c256714146ef0c1b66b7b97

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(HOST, debug=DEBUG)
