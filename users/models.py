from django.contrib.auth.models import AbstractUser, User
from django.db import models


class Country(models.Model):
    alpha_2 = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f' {self.name} - ({self.country.name})'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    date_of_birth = models.DateField(help_text='Format: YYYY-MM-DD', null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=True)
    #country = CountryField(multiple=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True, default='avatar.png')
    interest = models.CharField(max_length=300, help_text='Indicate what contents will you like to write/read about on this blog.', null=True, blank=True)
    about_me = models.TextField(max_length=300, help_text='Write something about yourself, not more than 300 words', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

