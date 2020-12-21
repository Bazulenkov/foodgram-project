from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField()
    amount = models.PositiveSmallIntegerField()
    unit = models.CharField()


class Resipe(models.Model):

    class Tag(models.TextChoices):
        BREAKFAST = 'B', _('Breakfast')
        LUNCH = 'L', _('Lunch')
        DINNER = 'D', _('Dinner')

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField()
    image = models.ImageField()  # add parameters!!!
    text = models.TextField()
    ingredient = models.ManyToManyField(Ingredient)
    tag = models.CharField(choices=Tag.choices)  # https://docs.djangoproject.com/en/3.1/ref/models/fields/#enumeration-types
    duration = models.DurationField()
    # pub_date = models.DateTimeField("date published", auto_now_add=True)
    slug = models.SlugField(unique=True)
