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
        author_id = self.kwargs.get("author_id")
        return get_object_or_404(Author, id=author_id)


class AuthorEditView(UpdateView):
    model = Author
    template_jame = "core/author_edit.html"
    fields = ["name", "biography"]
    pk_url_kwarg = "author_id"

    def get_success_url(self):
        return reverse("author_detail", kwargs={"author_id": self.object.id})


class AuthorCreateView(CreateView):
    model = Author
    template_name = "core/author_edit.html"
    fields = ["name", "biography"]

    def get_success_url(self):
        return reverse("author_detail", kwargs={"author_id": self.object.id})
