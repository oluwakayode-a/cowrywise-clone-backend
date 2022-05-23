from django.db import models
from accounts.models import User
from utils.paystack_funcs import create_transfer_recipient


# Create your models here.
class BankDetails(models.Model):
    """
    Create customer once Bank Details are added.
    """
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField("Return account name from Paystack on account number verified", max_length=100, blank=True)
    account_number = models.CharField(max_length=20)
    bank = models.CharField(max_length=100, choices=BANKS)
    recipient_code = models.CharField("Recipient Code sent from Paystack", max_length=500, blank=True)


class Card(models.Model):
    """
    Reference to Card stored on Paystack. Don't store user card details if you are not authorized to.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Keeping this simple. Next time store the email from the user input
    authorization_code = models.CharField("Authorization Code sent from Paystack", max_length=500)
    last_digits = models.CharField("Last four digits of the card.", max_length=10)
    card_type = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    expiry_date = models.CharField(max_length=255)


