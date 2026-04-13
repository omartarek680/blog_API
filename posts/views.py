
from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import  ListCreateAPIView, RetrieveDestroyAPIView, CreateAPIView,ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CategorySerializer, CommentSerializer, PostSerializer, TagSerializer
from .models import Category, Tag, Comment, Post
from .permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404


class ListCreateTag(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CreateComment(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
   
        serializer.save(author=self.request.user)

class ListComments(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        
        return Comment.objects.filter(author=self.request.user)
    

class RetrieveUpdateDestroyComment(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()


class ListPosts(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class CreatePost(CreateAPIView):
  
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ListCreatePost(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "author",

    ]
    search_fields = [
        "author__first_name",
        "author__last_name",
        "title",
        "category__name",
    ]
    oerdering_fields = [
        "created_at",

    ]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RetrieveUpdateDestroyPost(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)