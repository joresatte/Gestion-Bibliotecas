from flask import Flask, json, request, jsonify
from flask_cors import CORS

from src.lib.utils import object_to_json
from src.domain.books import Book
from src.domain.loans import Loan


def create_app(repositories):
    app = Flask(__name__)
    CORS(app)

    @app.route("/", methods=["GET"])
    def hello_world():
        return "...magic!"

    @app.route("/api/info", methods=["GET"])
    def info_get():
        info = repositories["info"].get_info()
        return object_to_json(info)

    @app.route("/api/books", methods=["GET"])
    def books_get():
        all_books = repositories["books"].get_books()
        return object_to_json(all_books)

    @app.route("/api/books", methods=["POST"])
    def add_book():
        body = request.json
        book = Book(**body)
        repositories["books"].save(book)

        return ''

    @app.route("/api/books/<id>", methods=["GET"])
    def book_get_by_id(id):
        book = repositories["books"].get_book_by_id(id)
        return object_to_json(book)

    @app.route("/api/books/<id>", methods=["DELETE"])
    def book_delete_by_id(id):
        repositories["books"].delete(id)
        return ''

    @app.route("/api/books/<id>", methods=["POST"])
    def book_edit_by_id(id):
        body = request.json
        book = Book(**body)
        repositories["books"].edit(book)
        return ''

    @app.route("/api/users", methods=["GET"])
    def get_users():
        all_users = repositories["users"].get_users()
        return object_to_json(all_users)

    @app.route("/api/loans", methods=["POST"])
    def book_loans():
        body = request.json
        loan = Loan(**body)
        repositories["loans"].save(loan)
        return ''

    @app.route("/api/loans/<id>", methods=["GET"])
    def book_is_loaned(id):
        loan_book = repositories["loans"].is_loaned(id)
        if loan_book:
            return "", 200
        else:
            return "", 404

    @app.route("/api/loans/<id>", methods=["DELETE"])
    def loaned_book_deleted_by_loan_id(id):
        repositories["loans"].delete(id)
        return '', 200

    return app
