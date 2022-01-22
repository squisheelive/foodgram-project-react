from django.contrib import admin

from .models import User, Tag, Ingredient, Recipe, IngredientAmount


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


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'image', 'cooking_time')
    empty_value_display = '-пусто-'
    search_fields = ('author', 'ingredient', 'tag')
    list_filter = ('tag',)


admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
