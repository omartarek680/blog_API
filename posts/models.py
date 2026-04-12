import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def upload_to_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    dir_name = instance.__class__.__name__.lower()
    clean_filename = f"{uuid.uuid4.hex[:8]}{extension}"
    return os.path.join("uploads",dir_name, clean_filename )

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category_image = models.ImageField(upload_to=upload_to_path, blank=True, null=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "Categories"
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True ,on_delete=models.SET_NULL, related_name="posts")
    post_image = models.ImageField(upload_to=upload_to_path, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.first_name
