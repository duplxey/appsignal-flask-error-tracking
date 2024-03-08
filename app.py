from flask import Flask

app = Flask(__name__)


@app.route("/")
def index_view():
    return {
        "name": "appsignal-flask-error-tracking"
    }


if __name__ == "__main__":
    app.run()
