from django.shortcuts import render
from rest_framework import generics, mixins
from .models import Article, ArticleCategory
from .serializers import ArticleSerializer, ArticleDetailSerializer, ArticleCategorySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.permissions import IsAuthorOrReadOnly, IsRegularMemberOrAdmin
from rest_framework import authentication

class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        category = serializer.validated_data.get("category")
        if category is None:
            category = ArticleCategory.objects.filter(id=6).first()
        serializer.save(author=self.request.user, category=category)


class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticated]


class ArticleUpdateAPIView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    

class ArticleDeleteAPIView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthorOrReadOnly]


    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        message = "Are you sure you want to delete this article?"
        data = {
            "message": message,
            "id": instance.id,
            "title": instance.title,
            "content": instance.content
        }
        return Response(data)


    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


#can be implemented in frontend next to form line for choosing category
#the idea is to be like +Add new category button
class ArticleCategoryCreateAPIView(generics.CreateAPIView):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer
    permission_classes = [IsRegularMemberOrAdmin]
