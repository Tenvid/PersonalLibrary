from django.urls import path
from .views import books, authors, publishers
from core._views import authors as author_views
from core._views import publishers as publisher_views
from core._views import books as book_html_views

urlpatterns = [
    path("", book_html_views.IndexView.as_view(), name="index"),
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
    path("api/authors/create/", authors.create),
    path("api/authors/update/<int:author_id>/", authors.update),
    path("api/authors/delete/<int:author_id>/", authors.delete),
    path("api/publishers/", publishers.read_all),
    path("api/publishers/<int:publisher_id>/", publishers.read_one),
    path("api/publishers/create/", publishers.create),
    path("api/publishers/update/<int:publisher_id>/", publishers.update),
    path("api/publishers/delete/<int:publisher_id>/", publishers.delete),
    # HTML template endpoints
    path("books/", book_html_views.IndexView.as_view(), name="books"),
    path(
        "books/<int:book_id>/",
        book_html_views.BookDetailView.as_view(),
        name="book_detail",
    ),
    path(
        "books/edit/<int:book_id>/",
        book_html_views.BookEditView.as_view(),
        name="book_edit",
    ),
    path(
        "books/create/",
        book_html_views.BookCreateView.as_view(),
        name="book_create",
    ),
    path("authors/", author_views.AuthorsListView.as_view(), name="authors"),
    path(
        "authors/create/",
        author_views.AuthorCreateView.as_view(),
        name="author_create",
    ),
    path(
        "authors/<slug:slug>/",
        author_views.AuthorDetailView.as_view(),
        name="author_detail",
    ),
    path(
        "authors/edit/<slug:slug>/",
        author_views.AuthorEditView.as_view(),
        name="author_edit",
    ),
    path(
        "publishers/", publisher_views.PublishersListView.as_view(), name="publishers"
    ),
    path(
        "publishers/create/",
        publisher_views.PublisherCreateView.as_view(),
        name="publisher_create",
    ),
    path(
        "publishers/<slug:slug>/",
        publisher_views.PublisherDetailView.as_view(),
        name="publisher_detail",
    ),
    path(
        "publishers/edit/<slug:slug>/",
        publisher_views.PublisherEditView.as_view(),
        name="publisher_edit",
    ),
]
