# Generated by Django 4.0.4 on 2022-05-21 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_rename_amount_savings_balance_savings_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='icon',
            field=models.ImageField(upload_to='icons/'),
        ),
        migrations.AlterField(
            model_name='savings',
            name='icon',
            field=models.ImageField(upload_to='icons/'),
        ),
    ]
