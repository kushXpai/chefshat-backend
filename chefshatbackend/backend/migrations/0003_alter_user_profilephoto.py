# Generated by Django 4.2.3 on 2023-07-16 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_user_profilephoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilePhoto',
            field=models.ImageField(null=True, upload_to='backend/profilePhotos'),
        ),
    ]