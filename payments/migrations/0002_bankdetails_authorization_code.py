# Generated by Django 4.0.4 on 2022-05-23 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankdetails',
            name='authorization_code',
            field=models.CharField(default='', max_length=500, verbose_name='Authorization Code sent from Paystack'),
        ),
    ]
