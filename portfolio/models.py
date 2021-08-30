from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1000)
    description = models.TextField(max_length=1000)
    features = models.TextField(max_length=10000, null=True, blank=True)
    github_link = models.URLField()
    demo_link = models.URLField()
    image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    show = models.BooleanField(default=False)
    date_published = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.TextField(max_length=100)

    def __str__(self):
        return self.title


class ContactMe(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.full_name}'
