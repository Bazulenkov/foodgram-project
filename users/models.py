from django.db import models
from django.contrib.auth.models import AbstractUser


class RecipeUser(AbstractUser):
    def __str__(self):
        fullname = self.get_full_name()
        if fullname:
            return fullname
        return self.username
