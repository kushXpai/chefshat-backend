# Generated by Django 4.2.3 on 2023-07-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_user_address_alter_user_dateofbirth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dateOfBirth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='emailAddress',
            field=models.EmailField(max_length=100),
        ),
    ]
