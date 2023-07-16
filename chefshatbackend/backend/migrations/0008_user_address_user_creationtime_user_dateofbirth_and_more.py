from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_remove_user_address_remove_user_dateofbirth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='user',
            name='creationTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user',
            name='dateOfBirth',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AddField(
            model_name='user',
            name='emailAddress',
            field=models.EmailField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='followings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='mobileNumber',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='profilePhoto',
            field=models.ImageField(null=True, upload_to='backend/profilePhotos'),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], default='MALE', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=255),
        ),
    ]
