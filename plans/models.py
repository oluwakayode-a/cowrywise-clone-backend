from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Investment(models.Model):
    TYPES = (
        ('naira', 'Naira'),
        ('usd', 'USD')
    )

    RISKS = (
        ('low', 'Low Risk'),
        ('high', 'High Risk'),
    )
    name = models.CharField(max_length=200)
    investment_type = models.CharField(max_length=20, choices=TYPES, default="naira")
    ytd_returns = models.CharField(max_length=10)
    risk_level = models.CharField(max_length=20, choices=RISKS)
    description = models.TextField()
    price_per_unit = models.IntegerField()
    icon = models.ImageField(upload_to="icons/")

    def __str__(self) -> str:
        return self.name


class Savings(models.Model):
    TYPES = (
        ('regular', 'Regular'),
        ('emergency', 'Emergency')
    )

    FREQ = (
        ("manual", "Manual"),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    savings_type = models.CharField(max_length=20, choices=TYPES, default='regular')
    description = models.TextField()
    icon = models.ImageField(upload_to="icons/")
    amount = models.IntegerField("Amount to be saved periodically (or the initial amount, if it's a manual option).")
    balance = models.IntegerField("Current balance left in the savings plan.")
    frequency = models.CharField(max_length=20, choices=FREQ, default="manual")


class UserInvestmentPlan(models.Model):
    """
    Investments are one time.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField()
    plan = models.ForeignKey(Investment, on_delete=models.CASCADE)