from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Create your models here.
    

class Stash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)


class Activity(models.Model):
    STATUSES = (
        ('processed', 'Processed'),
        ('redemption', 'Redemption'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Stash.objects.create(user=instance)