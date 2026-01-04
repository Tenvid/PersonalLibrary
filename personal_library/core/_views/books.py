from django.shortcuts import render
from django.core.paginator import Paginator
from core.models import Book


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
