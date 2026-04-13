from django.urls import path
from . import views

urlpatterns = [
    # Posts
    path("posts/", views.ListCreatePost.as_view(), name="list_create_posts"),
    path("posts/<int:pk>/", views.RetrieveUpdateDestroyPost.as_view(), name="post_detail"),

    # Tags
    path("tags/", views.ListCreateTag.as_view(), name="tags"),

    # Comments
    path("comments/", views.ListComments.as_view(), name="comment_list"),
    path("comments/create/", views.CreateComment.as_view(), name="comment_create"),
    path("comments/<int:pk>/", views.RetrieveUpdateDestroyComment.as_view(), name="comment_detail"),
]