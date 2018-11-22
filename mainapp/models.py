from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import User
from mptt.models import TreeForeignKey, MPTTModel
import mptt


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, verbose_name='User name')
    surname = models.CharField(max_length=100, verbose_name='User surname')
    telephone = models.CharField(max_length=10, blank=False, verbose_name='User telephone')
    email = models.EmailField()

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)


class Files(models.Model):

    def get_file_path(self, filename):
        return '{}/{}'.format(datetime.strftime(datetime.now(), '%Y_%m_%d'), filename)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=False)
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)



class TechnicalTask(models.Model):
    pub_date = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=False)
    theme = models.CharField(max_length=400, verbose_name='Theme of the task')
    description = models.TextField()

    def __str__(self):
        return 'Task: {}'.format(self.theme)


class Replies(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    file = models.ForeignKey(Files, on_delete=models.CASCADE, blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now())
    message = models.TextField(verbose_name='Replies to the task')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        ordering = ['pub_date', ]
