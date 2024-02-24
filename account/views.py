from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

#logout
from django.contrib.auth import logout
from rest_framework import views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated



# Create your views here.


User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()  

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email)
        if user is not None and user.check_password(password):
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                serializer = UserSerializer(user)
                return Response({'detail': 'Login successful', 'user': serializer.data, 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        


class UserLogoutView(views.APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
