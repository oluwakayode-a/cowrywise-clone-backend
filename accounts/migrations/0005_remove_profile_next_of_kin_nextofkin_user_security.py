# Generated by Django 4.0.4 on 2022-05-20 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_next_of_kin_alter_nextofkin_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='next_of_kin',
        ),
        migrations.AddField(
            model_name='nextofkin',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('two_fa', models.BooleanField(default=False)),
                ('pin', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
