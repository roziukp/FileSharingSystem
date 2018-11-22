from django.contrib import admin
from . import models


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email']


class FilesAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(models.Files, FilesAdmin)
admin.site.register(models.Profile,)
