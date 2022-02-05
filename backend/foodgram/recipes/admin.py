from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag, User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    empty_value_display = '-пусто-'
    list_filter = ('measurement_unit',)
    search_fields = ('name',)


# class IngredientAmountAdmin(admin.ModelAdmin):
#     list_display = ('ingredient', 'amount')
#     empty_value_display = '-пусто-'


class IngredientInline(admin.StackedInline):
    model = IngredientAmount


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'author', 'name', 'in_favorite')
    empty_value_display = '-пусто-'
    search_fields = ('author', 'ingredients', 'tags')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)
    inlines = [IngredientInline, ]
    readonly_fields = ('in_favorite',)

    def in_favorite(self, obj):
        return obj.favorite.all().count()

    in_favorite.short_description = 'В избранном'


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
# admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
