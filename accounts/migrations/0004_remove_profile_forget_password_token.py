# Generated by Django 4.0.4 on 2022-05-20 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='forget_password_token',
        ),
    ]
