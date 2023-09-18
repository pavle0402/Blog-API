from django.shortcuts import render
from articles.models import Article
from rest_framework.decorators import api_view
from articles.serializers import ArticleSerializer
from rest_framework.response import Response


@api_view(["POST"])
def api_home_view(request, *args, **kwargs):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print(serializer.data)

    return Response(serializer.data)


