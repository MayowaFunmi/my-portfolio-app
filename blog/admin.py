from django.contrib import admin
from .models import Post, Comment, Category

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)

admin.site.site_header = 'My Porfolio Admin Page'