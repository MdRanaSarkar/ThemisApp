from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(('email address'), unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = ['username']

class UserProfile(models.Model):
    USERDESIGNATION = (
        ("1", "NormalUser"),
        ("2", "Attorney"),
        )
    GENDERCHOICES = (
       ("Female", "Female"),
        ("Male", "Male"),
        ("Other", "Other"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    usergender = models.CharField(max_length=10, choices = GENDERCHOICES)
    designation = models.CharField(max_length=1, choices = USERDESIGNATION)
    
    
    def __str__(self):
        return self.phone_number
    

    