import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager




def upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4().hex[:8]}{ext}"
    return os.path.join("accounts", filename)
class CustomrUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email Is Required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None , **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Is Staff Must be True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Is_superuser Must Be True")

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, db_index=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomrUserManager()

    def __str__(self):
        return self.email