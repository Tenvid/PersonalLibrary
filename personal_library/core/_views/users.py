from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import User
from core.models import Rental


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        rentals = Rental.objects.filter(user=user).select_related("book").order_by("-rented_at")
        context["user"] = user
        context["rentals"] = rentals
        return context


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Username",
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
            "password1": "Password",
            "password2": "Confirm Password",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": placeholders.get(name, ""),
                }
            )


class RegisterUserCreateView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = "users/register.html"
    success_url = reverse_lazy("/books/")

    def form_valid(self, form):
        response = super().form_valid(form)
        # You can add any additional logic here if needed
        login(self.request, self.object)
        return response
