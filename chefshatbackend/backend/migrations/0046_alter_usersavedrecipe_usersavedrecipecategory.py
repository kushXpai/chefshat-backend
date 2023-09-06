# Generated by Django 4.2.3 on 2023-09-05 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0045_usersavedrecipe_usersavedrecipecategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersavedrecipe',
            name='UserSavedRecipeCategory',
            field=models.CharField(choices=[('appetizers', 'Appetizers'), ('entree', 'Entree'), ('desserts', 'Desserts'), ('sides', 'Sides'), ('snacks', 'Snacks')], max_length=200),
        ),
    ]
