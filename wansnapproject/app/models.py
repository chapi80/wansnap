from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, username=username, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'user'
        
class Dog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dogs')
    dog_name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('男の子','男の子'), ('女の子','女の子')])
    birthday = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    dog_image = models.ImageField(upload_to='dog_image/', null=True, blank=True)
    
    @property
    def age_months(self):
        if self.birthday:
            today = date.today()
            diff = relativedelta(today, self.birthday)
            return diff.years * 12 + diff.months
        return None
    
    def __str__(self):
        return f"{self.dog_name}({self.owner.username}のうちの子)"

class Post(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='posts')
    dog_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='post_images/')
    caption = models.TextField(blank=True)
    memo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    
@receiver(post_delete, sender=Post)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)