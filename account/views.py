from rest_framework.authtoken.models import Token

from django.shortcuts import render

from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from account.serializers import RegisterSerializer


class RegisterView(APIView):
    """
    Blog API endpoint to get list of blogs and create blogs
    """
    queryset = User.objects.all()
    serializers_class = RegisterSerializer

    def post(self, request):
        serializers = RegisterSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    queryset = User.objects.all()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK, )
            else:
                return Response({'detail': 'User account is not active'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)