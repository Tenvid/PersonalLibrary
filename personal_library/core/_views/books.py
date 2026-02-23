from core.models import Author, Book, Publisher
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
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


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "core/book_detail.html"
    context_object_name = "book"

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Book, slug=slug)


class BookEditView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = "core/book_edit.html"
    fields = [
        "title",
        "synopsis",
        "publication_date",
        "author",
        "publisher",
        "cover_image",
        "slug",
    ]
    # pk_url_kwarg = "book_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.all()
        context["publishers"] = Publisher.objects.all()
        return context

    def get_success_url(self):
        return reverse("book_detail", kwargs={"slug": self.object.slug})


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = "core/book_edit.html"
    fields = [
        "title",
        "synopsis",
        "publication_date",
        "author",
        "publisher",
        "cover_image",
        "slug",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = Author.objects.all()
        context["publishers"] = Publisher.objects.all()
        return context

    def get_success_url(self):
        return reverse("book_detail", kwargs={"slug": self.object.slug})


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "core/book_confirm_delete.html"

    def get_object(self):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Book, slug=slug)

    def get_success_url(self):
        return reverse("books")
