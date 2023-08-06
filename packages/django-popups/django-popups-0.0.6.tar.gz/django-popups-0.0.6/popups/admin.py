from django.contrib import admin
from .models import NotiPopups, EventPopups, ImagePopups

import django.contrib.auth.models
from django.contrib import auth


class PopupsAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'activate')
    search_fields = ['title']


admin.site.register(NotiPopups, PopupsAdmin)
admin.site.register(EventPopups, PopupsAdmin)
admin.site.register(ImagePopups, PopupsAdmin)

try:
    admin.site.unregister(auth.models.User)
    admin.site.unregister(auth.models.Group)
except django.contrib.admin.sites.NotRegistered:
    pass
