from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.manager import UserManager
from utils.base_model import BaseModel

# Create your models here.


class User(BaseModel, AbstractUser):
    username = models.CharField(max_length=40, unique=True, editable=False)
    email = models.EmailField(max_length=40, unique=True, blank=True, null=True, editable=False)
    id_number = models.CharField(max_length=40, unique=True, null=True, blank=True, editable=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='hostel_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='hostel_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        
        super().save(*args, **kwargs)
        
    

    objects=UserManager()
    USERNAME_FIELD ='username'
    REQUIRED_FIELDS=[]

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
        ]
    
    def __str__(self):
        return f"{self.username}"
