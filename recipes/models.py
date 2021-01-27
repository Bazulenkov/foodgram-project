from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .utils import slugify

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента."""

    title = models.CharField(
        verbose_name="Название ингредиента", max_length=50
    )
    dimension = models.CharField(
        verbose_name="Единица измерения", max_length=10
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Tag(models.Model):
    """Модель тэга."""

    title = models.CharField(max_length=8)
    slug = models.SlugField(unique=True, max_length=50, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    title = models.CharField(verbose_name="Название рецепта", max_length=50)
    tags = models.ManyToManyField(
        Tag, verbose_name="Тэги", related_name="recipes"
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient"
    )
    description = models.TextField(verbose_name="Описание")
    duration = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления"
    )
    image = models.ImageField(upload_to="recipes/")
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_view", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            same_slug_last = Recipe.objects.filter(
                slug__startswith=slug
            ).aggregate(models.Max("slug"))
            if same_slug_last["slug__max"]:
                slug = same_slug_last["slug__max"] + "1"
            self.slug = slug
        super().save(*args, **kwargs)


class RecipeIngredient(models.Model):
    """
    Модель, связывающая рецепт и ингредиент.

    В этой таблице будет хранится кол-во ингредиента в рецепте.
    """

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()

    class Meta:
        # в одном рецепте не может один ингредиент встречаться несколько раз
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        name = (
            f"{self.ingredient.title} - {self.amount} "
            f"{self.ingredient.dimension}"
        )
        return name


class Follow(models.Model):
    """Модель подписки на авторов."""

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
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        unique_together = ["user", "recipe"]

    def __str__(self):
        return f"{self.user}-{self.recipe}"
