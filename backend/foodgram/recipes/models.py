from django.contrib.auth import get_user_model
from django.db import models
from colorfield.fields import ColorField

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
    color = ColorField(default='#00ff80')

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



class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='following')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  blank=True, null=True,
                                  related_name='user')

class Favorite(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

class ShopList(models.Model):
    ...



