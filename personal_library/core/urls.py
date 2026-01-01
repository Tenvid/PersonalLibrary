from django.urls import path
from .views import books, authors

urlpatterns = [
    path("books/", books.read_all),
    path("books/create/", books.create),
    path("books/delete/<int:book_id>/", books.delete),
    path("books/<int:book_id>/", books.read_one),
    path("books/update/<int:book_id>/", books.update),
    path("authors/", authors.read_all),
    path("authors/<int:author_id>/", authors.read_one),
]
