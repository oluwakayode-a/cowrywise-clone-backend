# Generated by Django 4.0.4 on 2022-05-21 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0004_alter_investment_icon_alter_savings_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='savings',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='Amount to be saved periodically.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='savings',
            name='frequency',
            field=models.CharField(choices=[('manual', 'Manual'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=20),
        ),
    ]