from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    


class Profile(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="images/", blank=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER)
    visibility = models.BooleanField(default=False)


class NextofKin(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER)
    relationship = models.CharField(max_length=100, help_text="Father, Mother, etc.")
    # bank_details ==> when the payments app is done.