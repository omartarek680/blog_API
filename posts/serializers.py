from rest_framework import serializers
from .models import Post, Category, Tag, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "content", "author","post")


class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ("id", "name", "created_at")

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")



class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field = "name",
        queryset=Tag.objects.all()
    )
    comments = CommentSerializer(many=True,read_only=True)
    category = serializers.SlugRelatedField(
        slug_field = 'name',
        queryset = Category.objects.all()
    )
    class Meta:
        model = Post
        fields = ("id", "title", "content","author","comments","category","tags","created_at")

