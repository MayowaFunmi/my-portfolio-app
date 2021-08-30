from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment, Category
from portfolio.serializers import RegisterSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'body', 'post', 'created', 'updated']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True)
    #category = serializers.StringRelatedField(many=True)
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ['id', 'user', 'category', 'title', 'body', 'comments', 'created']


class CategorySerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')
    #posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #categories = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'posts', 'comments']

'''
# for nested serializer
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = RegisterSerializer(instance.user).data
        return response
'''