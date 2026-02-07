from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from core.models import Book, Author, Publisher
from django.views.generic.list import ListView


class IndexView(ListView):
    model = Book
    template_name = "core/index.html"
    context_object_name = "books"
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return Book.objects.filter(title__icontains=query).select_related(
                "author", "publisher"
            )
        return Book.objects.all().select_related("author", "publisher")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "core/book_detail.html"
    context_object_name = "book"

    def get_object(self):
        book_id = self.kwargs.get("book_id")
        return get_object_or_404(Book, id=book_id)


def index(request):
    # Get the search query from the request
    query = request.GET.get("q", "")

    # Get all books or filter based on the search query
    if query:
        books_list = Book.objects.filter(title__icontains=query).select_related(
            "author", "publisher"
        )
    else:
        books_list = Book.objects.all().select_related("author", "publisher")

    # Paginate the results (10 books per page)
    paginator = Paginator(books_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "books": page_obj,
        "query": query,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    }

    return render(request, "core/index.html", context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {"book": book}
    return render(request, "core/book_detail.html", context)


def book_edit(request, book_id=None):
    if book_id:
        book = get_object_or_404(Book, id=book_id)
        is_new = False
    else:
        book = None
        is_new = True

    if request.method == "POST":
        title = request.POST.get("title")
        synopsis = request.POST.get("synopsis")
        publication_date = request.POST.get("publication_date")

        # Handle author
        author_id = request.POST.get("author")
        author = None
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                author = None

        # Handle publisher
        publisher_id = request.POST.get("publisher")
        publisher = None
        if publisher_id:
            try:
                publisher = Publisher.objects.get(id=publisher_id)
            except Publisher.DoesNotExist:
                publisher = None

        if book:
            # Update existing book
            book.title = title
            book.synopsis = synopsis
            book.publication_date = publication_date
            book.author = author
            book.publisher = publisher

            # Handle cover image
            if "cover_image" in request.FILES:
                book.cover_image = request.FILES["cover_image"]
        else:
            # Create new book
            book = Book.objects.create(
                title=title,
                synopsis=synopsis,
                publication_date=publication_date,
                author=author,
                publisher=publisher,
            )

            # Handle cover image for new book
            if "cover_image" in request.FILES:
                book.cover_image = request.FILES["cover_image"]

        book.save()
        return redirect(
            "book_detail", book_id=book.id
        )  # Redirect to the book detail page

    # For GET request, show the form
    authors = Author.objects.all()
    publishers = Publisher.objects.all()

    context = {
        "book": book,
        "authors": authors,
        "publishers": publishers,
        "is_new": is_new,
    }
    return render(request, "core/book_edit.html", context)
