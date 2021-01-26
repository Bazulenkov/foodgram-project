from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    """Регистрация нового пользователя."""

    form_class = CreationForm
    success_url = reverse_lazy("index")
    template_name = "signup.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model and login."""
        # Переписал этот метод, чтобы сразу после регистрации пользователь
        # становился залогиненным.
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
