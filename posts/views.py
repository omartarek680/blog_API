from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListCreateAPIView, 
    RetrieveUpdateDestroyAPIView, 
    CreateAPIView, 
    ListAPIView
)
from .serializers import CategorySerializer, CommentSerializer, PostSerializer, TagSerializer
from .models import Category, Tag, Comment, Post
from .permissions import IsAuthorOrReadOnly

class ListCreateTag(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        # Only shows comments made by the logged-in user
        return Comment.objects.filter(author=self.request.user)

class RetrieveUpdateDestroyComment(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Comment.objects.all()

class ListCreatePost(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ["author", "category"] # Added category filter
    search_fields = ["author__first_name", "author__last_name", "title", "category__name"]
    ordering_fields = ["created_at"] # Fixed typo

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RetrieveUpdateDestroyPost(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]