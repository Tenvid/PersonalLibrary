from core.models import Book, Rental, RentalStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView


class ReturnRentalView(LoginRequiredMixin, UpdateView):
    model = Rental
    fields = []

    def get_object(self, queryset=None):
        return get_object_or_404(
            Rental, id=self.kwargs["rental_id"], user=self.request.user
        )

    def form_valid(self, form):
        self.object.returned_at = timezone.now()

        if self.object.returned_at <= self.object.expected_return_date:
            self.object.status = RentalStatus.ON_TIME.value
        else:
            self.object.status = RentalStatus.LATE.value

        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_profile")


class RentalCreateView(LoginRequiredMixin, CreateView):
    model = Rental
    template_name = "core/rental_form.html"
    fields = ["book"]

    def get_success_url(self):
        return reverse("user_profile")

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

        # If there is already a rental with the book that hasn't been returned, show an error
        if Rental.objects.filter(
            book=form.instance.book, status=RentalStatus.RENTED.value
        ).exists():
            form.add_error(
                "book", "This book is currently rented, please, select another one."
            )
            return self.form_invalid(form)
        return super().form_valid(form)


class RentalListView(LoginRequiredMixin, ListView):
    model = Rental
    template_name = "core/rental_list.html"
    context_object_name = "rentals"

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)
