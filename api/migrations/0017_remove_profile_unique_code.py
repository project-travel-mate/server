# Generated by Django 2.0.5 on 2018-07-29 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_profile_unique_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='unique_code',
        ),
    ]
