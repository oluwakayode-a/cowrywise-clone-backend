from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Create your models here.
class BankDetails(models.Model):
    BANKS = (
        ("044", "Access Bank"),
        ("063", "Access Bank (Diamond)"),
        ("050", "Ecobank Nigeria"),
        ("070", "Fidelity Bank"),
        ("011", "First Bank of Nigeria"),
        ("214", "First City Momument Bank"),
        ("058", "Guaranty Trust Bank"),
        ("50211", "Kuda Bank"),
        ("076", "Polaris Bank"),
        ("125", "Rubies MFB"),
        ("221", "Stanbic IBTC Bank"),
        ("068", "Standard Chatered Bank"),
        ("232", "Sterling Bank"),
        ("032", "Union Bank of Nigeria"),
        ("033", "United Bank for Africa"),
        ("215", "Unity Bank"),
        ("035", "Wema Bank"),
        ("057", "Zenith Bank")
    )
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    bank = models.CharField(max_length=100, choices=BANKS)
    

class Stash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    account_details = models.ForeignKey(BankDetails, on_delete=models.CASCADE, blank=True, null=True)


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