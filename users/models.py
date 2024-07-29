from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user    
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True, null=True, verbose_name="Avatar")
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    objects = UserManager()
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "email"]

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"
    
    def __str__(self):
        return self.username
