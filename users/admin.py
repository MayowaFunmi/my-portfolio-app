from django.contrib import admin

# Register your models here.
from .models import Profile, Country, City

admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(City)