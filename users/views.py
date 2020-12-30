from django.contrib.auth import login
from django.views.generic import CreateView

#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    # где login — это параметр "name" в path()
    success_url = reverse_lazy("index")
    template_name = "signup.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model and login"""
        # Переписал этот метод, чтобы сразу после регистрации пользователь
        # становился залогиненным.
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
