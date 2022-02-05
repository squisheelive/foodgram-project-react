from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_amount, validate_time


class User(AbstractUser):

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Tag(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='тэг'
    )
    color = ColorField(
        default='#00ff80',
        verbose_name='цвет'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='слаг'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='название'
    )
    measurement_unit = models.CharField(
        max_length=256,
        verbose_name='единица измерения'
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='название'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='тэги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='ингредиент'
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='изображение'
    )
    text = models.TextField(verbose_name='текст')
    cooking_time = models.IntegerField(
        validators=[validate_time],
        verbose_name='время приготовления'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientAmount(models.Model):

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент'
    )
    amount = models.IntegerField(
        validators=[validate_amount],
        default=1,
        verbose_name='количество'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ing_amount'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount} '
                f'{self.ingredient.measurement_unit}')


class Favorite(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='favorite',
        verbose_name='рецепты'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shoplist',
        verbose_name='пользователь'
    )
    recipes = models.ManyToManyField(
        Recipe,
        related_name='shoplist',
        verbose_name='рецепты'

    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
