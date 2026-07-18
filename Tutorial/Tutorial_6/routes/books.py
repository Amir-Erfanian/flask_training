from flask import Blueprint

books = Blueprint("books", __name__, url_prefix="/books")


@books.route("/")
def home():
    return "Books Home"