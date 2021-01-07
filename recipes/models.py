from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента"""

    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10)


class Recipe(models.Model):
    """Модель рецепта"""

    class Tag(models.TextChoices):
        BREAKFAST = "B", _("Breakfast")
        LUNCH = "L", _("Lunch")
        DINNER = "D", _("Dinner")

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(max_length=50)
    image = models.ImageField()  # add parameters!!!
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient"
    )
    tag = models.CharField(
        max_length=10, choices=Tag.choices
    )  # https://docs.djangoproject.com/en/3.1/ref/models/fields/#enumeration-types
    duration = models.DurationField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    slug = models.SlugField(unique=True, auto_created=True)

    class Meta:
        # в одном рецепте не может один ингредиент встречаться несколько раз
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["ingredients"], name="unique_ingredient"
        #     )
        # ]

        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('reсipe', kwargs={'slug': self.slug})


class RecipeIngredient(models.Model):
    """
    Модель, связывающая рецепт и ингредиент, \
     в этой таблице будет хранится кол-во ингредиента в рецепте.
    https://docs.djangoproject.com/en/3.1/topics/db/models/#extra-fields-on-many-to-many-relationships
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    class Meta:
        # в одном рецепте не может один ингредиент встречаться несколько раз
        unique_together = ["recipe", "ingredient"]


class Follow(models.Model):
    """Модель подписки на авторов"""

    # можно попробовать переопределить модель User и туда вставить
    # follower = models.ManyToManyField("self", symmetrical=False)
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ManyToManyField.symmetrical

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        unique_together = ["user", "author"]

    def __str__(self):
        return f"{self.user}-{self.author}"


class Favorite(models.Model):
    """Модель избранных рецептов"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "recipe"]

    def __str__(self):
        return f"{self.user}-{self.recipe}"
