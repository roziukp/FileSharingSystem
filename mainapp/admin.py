from django.contrib import admin
from . import models


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email']


# class FilesAdmin(admin.ModelAdmin):
#     list_display = ['user']

class TechnicalTaskAdmin(admin.ModelAdmin):
    list_display = ['theme', 'description', 'pub_date', 'user']


class RepliesAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'pub_date']

admin.site.register(models.Files)
admin.site.register(models.Profile,)
admin.site.register(models.TechnicalTask, TechnicalTaskAdmin)
admin.site.register(models.Replies, RepliesAdmin)
