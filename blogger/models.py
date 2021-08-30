from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=250)

    def get_absolute_url(self):
        return reverse('blogger:post_list')

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    post_image = models.ImageField(upload_to='blog_pics/%Y/%m/%d/', default='avatar.png')
    body = RichTextField()
    categories = models.CharField(max_length=250)
    likes = models.ManyToManyField(User, related_name='blog_post')
    publish = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blogger:post_detail',
                       args=[self.id,
                             self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'