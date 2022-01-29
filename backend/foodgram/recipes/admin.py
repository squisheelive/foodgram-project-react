from django.contrib import admin

from .models import (User, Tag, Ingredient,
                     Recipe, IngredientAmount,
                     Follow, Favorite, ShoppingCart)


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    empty_value_display = '-пусто-'
    search_fields = ('name',)


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')
    empty_value_display = '-пусто-'


class IngredientInline(admin.StackedInline):
    model = IngredientAmount


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'image', 'cooking_time')
    empty_value_display = '-пусто-'
    search_fields = ('author', 'ingredients', 'tags')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)
    inlines = [IngredientInline, ]


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ['recipes', ]


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ['recipes', ]


admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
