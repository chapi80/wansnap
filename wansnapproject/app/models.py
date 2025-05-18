from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser, PermissionsMixin
)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'user'
        
class Dog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dogs')
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('男の子','男の子'), ('女の子','女の子')])
    birthday = models.DateField(null=True, blank=True)
    dog_image = models.ImageField(upload_to='dog_image/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}({self.owner.username}のうちの子)"