from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField
from .validators import validate_amount, validate_time


class User(AbstractUser):

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='user'
    )


class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True)
    color = ColorField(default='#00ff80')
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes'
    )
    image = models.ImageField(upload_to='images/')
    text = models.TextField()
    cooking_time = models.IntegerField(validators=[validate_time])


class IngredientAmount(models.Model):

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        validators=[validate_amount],
        default=1
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount} '
                f'{self.ingredient.measurement_unit}')


class Favorite(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ManyToManyField(Recipe)


class ShopList(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shoplist'
    )
    recipe = models.ManyToManyField(Recipe)
