from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name= "register"),
    path('login/', views.login, name= "login"),
    path('logout/', views.logout, name= "logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("change-password/", views.ChangePassword.as_view(), name="change_password"),
    path("request-reset/", views.RequestResetPassword.as_view(), name="request_reset"),
    path("confirm-rest/<uidb64>/<token>/", views.ConfirmResetView.as_view(), name="confirm_reset")

]
