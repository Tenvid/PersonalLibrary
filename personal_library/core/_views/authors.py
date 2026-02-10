from core.models import Author
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
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


class AuthorDetailView(DetailView):
    model = Author
    template_name = "core/author_detail.html"
    context_object_name = "author"

    def get_object(self):
        author_slug = self.kwargs.get("slug")
        return get_object_or_404(Author, slug=author_slug)


class AuthorEditView(UpdateView):
    model = Author
    template_name = "core/author_edit.html"
    fields = ["name", "biography", "slug"]
    pk_url_kwarg = "slug"

    def get_object(self):
        author_slug = self.kwargs.get("slug")
        return get_object_or_404(Author, slug=author_slug)

    def get_success_url(self):
        return reverse("author_detail", kwargs={"slug": self.object.slug})


class AuthorCreateView(CreateView):
    model = Author
    template_name = "core/author_edit.html"
    fields = ["name", "biography", "slug"]

    def get_success_url(self):
        return reverse("author_detail", kwargs={"slug": self.object.slug})
