from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from core.models import Book, Author, Publisher


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
    context = {
        'book': book
    }
    return render(request, 'core/book_detail.html', context)


def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # Update book with POST data
        book.title = request.POST.get('title')
        book.synopsis = request.POST.get('synopsis')
        book.publication_date = request.POST.get('publication_date')

        # Handle author
        author_id = request.POST.get('author')
        if author_id:
            book.author = get_object_or_404(Author, id=author_id)

        # Handle publisher
        publisher_id = request.POST.get('publisher')
        if publisher_id:
            book.publisher = get_object_or_404(Publisher, id=publisher_id)
        else:
            book.publisher = None

        # Handle cover image
        if 'cover_image' in request.FILES:
            book.cover_image = request.FILES['cover_image']

        book.save()
        return redirect('book_detail', book_id=book.id)  # Redirect to the book detail page

    # For GET request, show the edit form
    authors = Author.objects.all()
    publishers = Publisher.objects.all()

    context = {
        'book': book,
        'authors': authors,
        'publishers': publishers
    }
    return render(request, 'core/book_edit.html', context)
