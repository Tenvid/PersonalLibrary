from core.models import Book, Rental, RentalStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class RentalCreateView(LoginRequiredMixin, CreateView):
    model = Rental
    template_name = "core/rental_form.html"
    fields = ["book"]

    def get_success_url(self):
        return reverse("rentals")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_book = Book.objects.filter(slug=self.request.GET.get("book")).first()

        rented_books = Rental.objects.filter(
            status=RentalStatus.RENTED.value
        ).values_list("book_id", flat=True)

        if selected_book.id not in rented_books:
            context["selected_book"] = selected_book
        else:
            context["error"] = (
                "This book is currently rented, please, select another one."
            )

        context["books"] = Book.objects.exclude(id__in=rented_books)

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = RentalStatus.RENTED.value
        return super().form_valid(form)


class RentalListView(LoginRequiredMixin, ListView):
    model = Rental
    template_name = "core/rental_list.html"
    context_object_name = "rentals"

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)
