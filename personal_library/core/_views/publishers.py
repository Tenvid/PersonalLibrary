from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from core.models import Publisher


def publishers_html(request):
    # Get the search query from the request
    query = request.GET.get("q", "")

    # Get all publishers or filter based on the search query
    if query:
        publishers_list = Publisher.objects.filter(name__icontains=query)
    else:
        publishers_list = Publisher.objects.all()

    # Paginate the results (8 publishers per page)
    paginator = Paginator(publishers_list, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "publishers": page_obj,
        "query": query,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    }

    return render(request, "core/publishers.html", context)


def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    context = {"publisher": publisher}
    return render(request, "core/publisher_detail.html", context)


def publisher_edit(request, publisher_id=None):
    if publisher_id:
        publisher = get_object_or_404(Publisher, id=publisher_id)
        is_new = False
    else:
        publisher = None
        is_new = True

    if request.method == "POST":
        # Update or create publisher with POST data
        name = request.POST.get("name")
        country = request.POST.get("country")

        if publisher:
            # Update existing publisher
            publisher.name = name
            publisher.country = country
            publisher.save()
        else:
            # Create new publisher
            publisher = Publisher.objects.create(name=name, country=country)

        return redirect(
            "publisher_detail", publisher_id=publisher.id
        )  # Redirect to the publisher detail page

    # For GET request, show the form
    context = {"publisher": publisher, "is_new": is_new}
    return render(request, "core/publisher_edit.html", context)

