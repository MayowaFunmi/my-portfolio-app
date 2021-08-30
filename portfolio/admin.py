from django.contrib import admin
from .models import Project, Book, ContactMe

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'features', 'github_link', 'demo_link', 'show', 'date_published', 'created_at']
    prepopulated_fields = {'slug': ['name']}

#admin.site.register(Project)
admin.site.register(Book)
admin.site.register(ContactMe)
admin.site.site_header = 'My Portfolio Website'