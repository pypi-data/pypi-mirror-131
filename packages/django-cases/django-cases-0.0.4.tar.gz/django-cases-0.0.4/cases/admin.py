from django.contrib import admin
from .models import Cases, Category

import django.contrib.auth.models
from django.contrib import auth


class CasesAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'filter')
    search_fields = ['title']


admin.site.register(Category)
admin.site.register(Cases, CasesAdmin)
try:
    admin.site.unregister(auth.models.User)
    admin.site.unregister(auth.models.Group)
except django.contrib.admin.sites.NotRegistered:
    pass

