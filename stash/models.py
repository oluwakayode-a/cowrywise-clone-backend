from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from transactions.models import StashTransaction

User = get_user_model()

# Create your models here.
    

class Stash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def record_transaction(self, reference, status, description):
        r, created = StashTransaction.objects.update_or_create(
            stash=self,
            reference=reference,
            status=status,
            description=description,
        )
        r.save()
        return True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Stash.objects.create(user=instance)