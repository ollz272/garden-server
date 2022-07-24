from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/sign_up.html"

    def form_valid(self, form):
        messages.success(
            self.request,
            f"The {form.instance} was created successfully. Please log-in below.",
        ),
        response = super().form_valid(form)
        return response


class UserLoginView(LoginView):
    success_url = "/"
    template_name = "accounts/login.html"

    def get_success_url(self):
        return self.success_url
