from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify as django_slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()

def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 
            'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 
            'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}
            
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class Ingredient(models.Model):
    """Модель ингредиента"""

    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10)


class Tag(models.Model):
    """Модель тэга"""

    title = models.CharField(max_length=8)
    slug = models.SlugField(unique=True, max_length=50, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """Модель рецепта"""

    # TAG_CHOICES = [
    #     ('breakfast', 'Breakfast'),
    #     ('lunch', 'Lunch'),
    #     ('dinner', 'Dinner')
    # ]

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(verbose_name="Название рецепта", max_length=50)
    tag = models.ManyToManyField(Tag, blank=True, related_name="recipes")
    # tag = models.CharField(max_length=100, choices=TAG_CHOICES)  # https://docs.djangoproject.com/en/3.1/ref/models/fields/#enumeration-types
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", related_name="recipes"
    )
    description = models.TextField(verbose_name="Описание")
    duration = models.PositiveSmallIntegerField(verbose_name="Время приготовления")
    image = models.ImageField(upload_to="recipes/")
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    slug = models.SlugField(unique=True)

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
        return reverse("reсipe_view", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


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
