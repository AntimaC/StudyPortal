# Generated by Django 4.0.4 on 2022-06-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_profile_date_joined_remove_profile_last_login_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='branch',
            field=models.CharField(max_length=100, verbose_name=''),
        ),
    ]