from django.contrib.auth.models import AbstractUser
from django.db import models


class RecipeUser(AbstractUser):
    def __str__(self):
        fullname = self.get_full_name()
        if fullname:
            return fullname
        return self.username
