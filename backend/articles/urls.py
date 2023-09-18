from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListCreateAPIView.as_view(), name='article-list-create'),
    path('<int:pk>/', views.ArticleDetailAPIView.as_view(), name='article-detail'),
    path('<int:pk>/update/', views.ArticleUpdateAPIView.as_view(), name='article-update'),
    path('<int:pk>/delete/', views.ArticleDeleteAPIView.as_view(), name='article-delete'),
    path('categories/create/', views.ArticleCategoryCreateAPIView.as_view(), name='article-category-create'),

]