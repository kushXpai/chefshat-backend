from rest_framework import serializers
from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'profilePhoto',
            'sex',
            'mobileNumber',
            'emailAddress',
            'dateOfBirth',
            'address',
            'followers',
            'followings',
            'creationTime'
            ]