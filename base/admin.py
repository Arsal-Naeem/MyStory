import imp
from django.contrib import admin

# Register your models here.
from .models import Story

admin.site.register(Story)