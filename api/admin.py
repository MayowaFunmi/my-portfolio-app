from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('title', 'description')