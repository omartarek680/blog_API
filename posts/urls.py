from django.urls import path
from . import views
urlpatterns = [

    path("tags/", views.ListCreateTag.as_view(), name="tags"),
    path("comments/", views.ListComments.as_view(), name="comment"),
    path("comments/create/", views.CreateComment.as_view(), name="comment_create"),
    path("comments/<int:pk>/", views.RetrieveUpdateDestroyComment.as_view(), name="retrieve_update_destroy_comment")
    
]
