from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Setup icons with Cloudinary.

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
    icon = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Savings(models.Model):
    TYPES = (
        ('regular', 'Regular'),
        ('halal', 'Halal'),
        ('emergency', 'Emergency')
    )

    FREQ = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    )
    savings_type = models.CharField(max_length=20, choices=TYPES, default='regular')
    description = models.TextField()
    icon = models.CharField(max_length=100)
    amount = models.IntegerField()
    frequency = models.CharField(max_length=20, choices=FREQ)


class UserInvestmentPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField()
    plan = models.ForeignKey(Investment, on_delete=models.CASCADE)


class UserSavingsPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Savings, on_delete=models.CASCADE)
