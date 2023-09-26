from rest_framework import serializers
from .models import User, UserUpload

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'profilePhoto',
            'mobileNumber',
            'followers',
            'followings',
            'creationTime'
            ]
        
class UserUploadSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserUpload
        fields = [
            'userId',
            'uploadLikes',
            'uploadImage',
            'uploadName',
            'uploadDescription',
            'creationTime',
            ]