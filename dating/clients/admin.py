from django.conf import settings
from django.contrib import admin

from .models import Client, Like


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'gender',
    )
    list_filter = ('gender',)
    search_fields = (
        'id',
        'email',
        'first_name',
        'last_name',
    )
    empty_value_display = settings.ADMIN_EMPTY_VALUE


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('matcher', 'matched', 'like')
    list_filter = ('like',)
    search_fields = ('matcher', 'matched')
