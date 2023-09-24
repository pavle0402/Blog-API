from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from api.permissions import IsAuthorOrReadOnly
from .models import ProfilePage, Hobbies
from .serializers import ProfilePageSerializer, ProfilePageDetailSerializer, RegistrationSerializer, LoginSerializer
from rest_framework import permissions
from api.authentication import TokenAuthentication
from rest_framework import serializers, status
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token




class ProfileCreateAPIView(generics.CreateAPIView):
    queryset = ProfilePage.objects.all()
    serializer_class = ProfilePageSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        bio = serializer.validated_data.get('bio') or None
        if bio is None:
            bio = f"User's bio is empty."
        if ProfilePage.objects.filter(author=user).exists():
            raise serializers.ValidationError("This user already has profile page created.")
        serializer.save(author=user, bio=bio)



class ProfileListAPIView(generics.ListAPIView):
    queryset = ProfilePage.objects.all()
    serializer_class = ProfilePageSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = ProfilePage.objects.all()
    serializer_class = ProfilePageDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = ProfilePage.objects.all()
    serializer_class = ProfilePageSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save(last_updated=timezone.now())
        return instance


class ProfileDeleteAPIView(generics.DestroyAPIView):
    queryset = ProfilePage.objects.all()
    serializer_class = ProfilePageSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    

#Authentication views
class RegisterUserAPIView(generics.CreateAPIView):
    model = User
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        if serializer.is_valid():
            user = serializer.save()
            new_user = self.serializer_class(user)
            return Response(new_user.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        request.auth.is_valid = False
        request.auth.save()
        logout(request)
        return Response({"message":"Logout successful."}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        return Response({"message":"You have successfully logged out."})
        