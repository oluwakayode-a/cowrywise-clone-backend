from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
GENDER = (
    ('male', 'Male'),
    ('female', 'Female')
)
class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="images/", blank=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER)
    visibility = models.BooleanField(default=False)


class NextofKin(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER)
    relationship = models.CharField(max_length=100, help_text="Father, Mother, etc.")
    # bank_details ==> when the payments app is done.