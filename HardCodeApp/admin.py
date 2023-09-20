from django.contrib import admin
from django.contrib.admin.sites import site

from HardCodeApp.models import Product, Access, Lesson, View

# Register your models here.

site.register(Product)
site.register(Access)
site.register(Lesson)
site.register(View)
