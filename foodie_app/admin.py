from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_added')
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)