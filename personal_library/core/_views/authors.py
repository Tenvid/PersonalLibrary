from django.shortcuts import render
from django.core.paginator import Paginator
from core.models import Author


def base(request):
    return render(request, "core/base.html")


def authors_html(request):
    # Get the search query from the request
    query = request.GET.get("q", "")

    # Get all authors or filter based on the search query
    if query:
        authors_list = Author.objects.filter(name__icontains=query)
    else:
        authors_list = Author.objects.all()

    # Paginate the results (9 authors per page)
    paginator = Paginator(authors_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "authors": page_obj,
        "query": query,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    }

    return render(request, "core/authors.html", context)