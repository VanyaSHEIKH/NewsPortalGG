from django.shortcuts import render
from rest_framework import viewsets, permissions

from .serializers import *
from .models import *


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class NewsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='N')
    serializer_class = NewsSerializer


class ArticleViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='A')
    serializer_class = ArticleSerializer


class PostCategoryViewset(viewsets.ModelViewSet):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
