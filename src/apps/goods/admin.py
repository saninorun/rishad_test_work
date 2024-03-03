from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title',)
    list_display_links = ('title',)
    ordering = ('id',)
