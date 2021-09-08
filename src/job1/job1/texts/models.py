from django import forms
from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    wholeTxt = models.FileField(upload_to = 'media/files/%Y/%m/%d/',verbose_name='Загрузите файл')

# Create your models here.
