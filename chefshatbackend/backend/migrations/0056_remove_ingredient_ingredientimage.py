# Generated by Django 4.2.3 on 2023-09-25 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0055_remove_user_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='ingredientImage',
        ),
    ]