from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='following')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  blank=True, null=True,
                                  related_name='user')


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(default='#00ff80')
    slug = models.SlugField(max_length=200, unique=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=256)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tag = models.ManyToManyField(Tag)
    ingredient = models.ManyToManyField(Ingredient)
    image = models.ImageField(upload_to='images/')
    text = models.TextField()
    cooking_time = models.IntegerField()


class Amount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    count = models.IntegerField()


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
