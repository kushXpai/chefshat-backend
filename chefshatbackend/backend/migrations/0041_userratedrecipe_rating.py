# Generated by Django 4.2.3 on 2023-07-29 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0040_rename_recipesaved_userratedrecipe_reciperated'),
    ]

    operations = [
        migrations.AddField(
            model_name='userratedrecipe',
            name='rating',
            field=models.CharField(choices=[('THUMBSUP', 'THUMBS UP'), ('THUMBSDOWN', 'THUMBS DOWN')], default='THUMBSUP', max_length=10),
        ),
    ]
