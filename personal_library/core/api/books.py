from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect
from core.models import Book


def read_all(request):
    books = Book.objects.all()
    books_data = [book.to_dict() for book in books]
    return JsonResponse(books_data, safe=False)


def create(request):
    from core.models import Author, Publisher

    def get_post_data():
        return {
            "title": request.POST.get("title"),
            "author_id": request.POST.get("author"),
            "publisher_id": request.POST.get("publisher"),
            "synopsis": request.POST.get("synopsis"),
            "publication_date": request.POST.get("publication_date"),
        }

    post_data = get_post_data()

    try:
        author = (
            Author.objects.get(id=post_data["author_id"])
            if post_data["author_id"]
            else None
        )
    except Author.DoesNotExist:
        author = None

    try:
        publisher = (
            Publisher.objects.get(id=post_data["publisher_id"])
            if post_data["publisher_id"]
            else None
        )
    except Publisher.DoesNotExist:
        publisher = None

    book = Book.objects.create(
        title=post_data["title"],
        author=author,
        publisher=publisher,
        synopsis=post_data["synopsis"],
        publication_date=post_data["publication_date"],
    )
    return redirect("/books/")


def delete(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return HttpResponse(status=204)
    except Book.DoesNotExist:
        return HttpResponse(status=404)


def update(request, book_id):
    from core.models import Author, Publisher

    def get_post_data():
        return {
            "title": request.POST.get("title"),
            "author_id": request.POST.get("author"),
            "publisher_id": request.POST.get("publisher"),
            "synopsis": request.POST.get("synopsis"),
            "publication_date": request.POST.get("publication_date"),
        }

    post_data = get_post_data()

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    try:
        author = (
            Author.objects.get(id=post_data["author_id"])
            if post_data["author_id"]
            else None
        )
    except Author.DoesNotExist:
        author = None

    try:
        publisher = (
            Publisher.objects.get(id=post_data["publisher_id"])
            if post_data["publisher_id"]
            else None
        )
    except Publisher.DoesNotExist:
        publisher = None

    book.title = post_data["title"]
    book.author = author
    book.publisher = publisher
    book.synopsis = post_data["synopsis"]
    book.publication_date = post_data["publication_date"]
    book.save()

    return redirect("/books/")


def read_one(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        return JsonResponse(book.to_dict())
    except Book.DoesNotExist:
        return HttpResponse(status=404)
