import os, flask

from flask import Flask

app = Flask(__name__)


@app.route
def index():
    return 'Привет от приложения фласк'


if __name__ == '__main__':
    port = int(os.environ.get('POST', 5000))
    app.run(host='0.0.0.0', port=port)
