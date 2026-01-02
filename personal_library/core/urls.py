from django.urls import path
from . import views
from .views import books, authors, publishers, book_views

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", books.read_all),
    path("books/create/", books.create),
    path("books/delete/<int:book_id>/", books.delete),
    path("books/<int:book_id>/", books.read_one),
    path("books/update/<int:book_id>/", books.update),
    path("books/author/<int:author_id>/", books.read_by_author),
    path("books/publisher/<int:publisher_id>/", books.read_by_publisher),
    path("authors/", authors.read_all),
    path("authors/<int:author_id>/", authors.read_one),
    path("publishers/", publishers.read_all),
    path("base/", book_views.base),
]
