from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.base_user import BaseUserManager


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
    
    def __str__(self):
        return f"{self.dog_name}({self.owner.username}のうちの子)"

class Post(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)