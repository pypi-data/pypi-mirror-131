from django.contrib import admin
from .models import ModelFavStock

import django.contrib.auth.models
from django.contrib import auth


class FavStockAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'remarks', 'red', 'point')
    search_fields = ['code', 'name']


admin.site.register(ModelFavStock)

try:
    admin.site.unregister(auth.models.User)
    admin.site.unregister(auth.models.Group)
except django.contrib.admin.sites.NotRegistered:
    pass


