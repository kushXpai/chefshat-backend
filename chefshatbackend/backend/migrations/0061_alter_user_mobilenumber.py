# Generated by Django 4.2.3 on 2023-09-26 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0060_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobileNumber',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
