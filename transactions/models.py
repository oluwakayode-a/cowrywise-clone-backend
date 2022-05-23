from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from stash.models import Stash


# Create your models here.
class PlanTransaction(models.Model):
    """
    Transaction History for Plan
    """
    TYPES = (
        ("deposit", "deposit"),
        ("withdrawal", "withdrawal")
    )

    STATUS = (
        ("failed", "failed"),
        ("pending", "pending"),
        ("processed", "processed")
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=20, choices=TYPES)
    reference = models.CharField("Reference from Paystack", max_length=20)
    status = models.CharField(max_length=20, choices=STATUS)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    triggered_by = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name_plural = "plan transactions"


class StashTransaction(models.Model):
    """
    Transaction History for Stash
    """
    TYPES = (
        ("transfer.plan", "transfer.plan"),
        ("transfer.bank", "transfer.bank"),
        ("topup", "topup")
    )

    STATUS = (
        ("failed", "failed"),
        ("pending", "pending"),
        ("processed", "processed")
    )
    stash = models.ForeignKey(Stash, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TYPES)
    reference = models.CharField("Reference from Paystack", max_length=20)
    status = models.CharField(max_length=20, choices=STATUS)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "stash transactions"