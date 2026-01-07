from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from core.models import Author


def authors_html(request):
    # Get the search query from the request
    query = request.GET.get("q", "")

    # Get all authors or filter based on the search query
    if query:
        authors_list = Author.objects.filter(name__icontains=query)
    else:
        authors_list = Author.objects.all()

    # Paginate the results (8 authors per page)
    paginator = Paginator(authors_list, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "authors": page_obj,
        "query": query,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    }

    return render(request, "core/authors.html", context)


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    context = {"author": author}
    return render(request, "core/author_detail.html", context)


def author_edit(request, author_id=None):
    if author_id:
        author = get_object_or_404(Author, id=author_id)
        is_new = False
    else:
        author = None
        is_new = True

    if request.method == "POST":
        # Update or create author with POST data
        name = request.POST.get("name")
        biography = request.POST.get("biography")

        if author:
            # Update existing author
            author.name = name
            author.biography = biography
            author.save()
        else:
            # Create new author
            author = Author.objects.create(name=name, biography=biography)

        return redirect(
            "author_detail", author_id=author.id
        )  # Redirect to the author detail page

    # For GET request, show the form
    context = {"author": author, "is_new": is_new}
    return render(request, "core/author_edit.html", context)

