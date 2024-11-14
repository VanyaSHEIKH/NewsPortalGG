from .models import *
from rest_framework import serializers


class PostCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['category']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    categories = PostCategorySerializer(many=True)
    rating = serializers.FloatField(read_only=True)
    date_in = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'post_type', 'date_in', 'rating',
                  'categories']  # categories - это релейтид нейм из модели посткатегори


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'post_type']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'category', 'title', 'text', 'post_type']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
