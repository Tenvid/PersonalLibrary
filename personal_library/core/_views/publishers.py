from django.shortcuts import render
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

    # Paginate the results (9 publishers per page)
    paginator = Paginator(publishers_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "publishers": page_obj,
        "query": query,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    }

    return render(request, "core/publishers.html", context)