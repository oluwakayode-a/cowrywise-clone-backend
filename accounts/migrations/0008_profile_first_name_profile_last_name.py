# Generated by Django 4.0.4 on 2022-05-20 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_profile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
