from django.http import JsonResponse
from .models import User
from .serializers import UserSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def UserList(request, format=None):
    serializer = UserSerializers(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   