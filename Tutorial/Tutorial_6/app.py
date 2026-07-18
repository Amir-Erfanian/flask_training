from flask import Flask
from routes.books import books

app = Flask(__name__)

app.register_blueprint(books)

if __name__ == '__main__':
    app.run(debug=True)
