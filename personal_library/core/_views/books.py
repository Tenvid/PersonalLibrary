from core.models import Author, Book, Publisher
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
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


class BookEditView(UpdateView):
    model = Book
    template_name = "core/book_edit.html"
    fields = [
        "title",
        "synopsis",
        "publication_date",
        "author",
        "publisher",
        "cover_image",
    ]
    pk_url_kwarg = "book_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.all()
        context["publishers"] = Publisher.objects.all()
        return context

    def get_success_url(self):
        return reverse("book_detail", kwargs={"book_id": self.object.id})


class BookCreateView(CreateView):
    model = Book
    template_name = "core/book_edit.html"
    fields = [
        "title",
        "synopsis",
        "publication_date",
        "author",
        "publisher",
        "cover_image",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.all()
        context["publishers"] = Publisher.objects.all()
        return context

    def get_success_url(self):
        return reverse("book_detail", kwargs={"book_id": self.object.id})
