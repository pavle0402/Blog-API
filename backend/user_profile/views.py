from django.shortcuts import render
from rest_framework import generics
from api.permissions import IsAuthorOrReadOnly
from .models import ProfilePage, Hobbies
from .serializers import ProfilePageSerializer, ProfilePageDetailSerializer
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.response import Response
from django.utils import timezone

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
    
