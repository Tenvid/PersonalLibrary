from django.urls import path
from . import views
from .views import books, authors, publishers
from core._views import authors as author_views
from core._views import publishers as publisher_views
from core._views import books as book_html_views

urlpatterns = [
    path("", book_html_views.index, name="index"),
    # API endpoints (return JSON)
    path("api/books/", books.read_all),
    path("api/books/create/", books.create),
    path("api/books/delete/<int:book_id>/", books.delete),
    path("api/books/<int:book_id>/", books.read_one),
    path("api/books/update/<int:book_id>/", books.update),
    path("api/books/author/<int:author_id>/", books.read_by_author),
    path("api/books/publisher/<int:publisher_id>/", books.read_by_publisher),
    path("api/authors/", authors.read_all),
    path("api/authors/<int:author_id>/", authors.read_one),
    path("api/publishers/", publishers.read_all),
    # HTML template endpoints
    path("books/", book_html_views.index, name="books"),
    path("books/<int:book_id>/", book_html_views.book_detail, name="book_detail"),
    path("books/edit/<int:book_id>/", book_html_views.book_edit, name="book_edit"),
    path("authors/", author_views.authors_html, name="authors"),
    path("publishers/", publisher_views.publishers_html, name="publishers"),
]
