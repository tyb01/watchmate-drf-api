from account_app.api.serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from account_app import models

@api_view(['POST'])
def RegisterView(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['Response'] = "Account registered successfully!"
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user = account)
            data['token'] = token.key
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def LogoutView(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(
            {"Response" : "You logged out successfully!"} , status= status.HTTP_200_OK
        )
