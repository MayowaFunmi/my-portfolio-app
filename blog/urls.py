from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
app_name = 'blog'

urlpatterns = [
    path('posts/', views.PostCreateList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('comments/', views.CommentCreateList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<int:pk>/', views.CategoryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)