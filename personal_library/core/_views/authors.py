from django.shortcuts import render, get_object_or_404, redirect
from core.models import Author
from django.views.generic.list import ListView


class AuthorsListView(ListView):
    model = Author
    template_name = "core/authors.html"
    context_object_name = "authors"
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return Author.objects.filter(name__icontains=query)
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


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
