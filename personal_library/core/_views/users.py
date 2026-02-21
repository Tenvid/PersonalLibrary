from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User


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
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        # You can add any additional logic here if needed
        login(self.request, self.object)
        return response
