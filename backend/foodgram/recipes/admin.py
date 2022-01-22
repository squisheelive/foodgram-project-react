from django.contrib import admin

from .models import User, Tag


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name')


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
