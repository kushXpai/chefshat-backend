# Generated by Django 4.2.3 on 2023-09-25 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0054_user_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
    ]
