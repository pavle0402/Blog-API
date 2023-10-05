from django.urls import path
from . import views

urlpatterns = [
    #article endpoints
    path('', views.ArticleListCreateAPIView.as_view(), name='article-list-create'),
    path('<int:pk>/', views.ArticleDetailAPIView.as_view(), name='article-detail'),
    path('<int:pk>/update/', views.ArticleUpdateAPIView.as_view(), name='article-update'),
    path('<int:pk>/delete/', views.ArticleDeleteAPIView.as_view(), name='article-delete'),
    path('categories/create/', views.ArticleCategoryCreateAPIView.as_view(), name='article-category-create'),
    #comment endpoints
    path('comments/', views.CommentListAPIView.as_view(), name='comment-list'),
    path('comments/create/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', views.CommentRetrieveAPIView.as_view(), name="comment-detail"),
    path('comments/<int:parent_comment_id>/replies/<int:pk>/', views.CommentRetrieveAPIView.as_view(), name="comment-detail"),
    path('comments/<int:pk>/delete', views.CommentDeleteAPIView.as_view(), name='comment-delete'),
    path('comments/<int:pk>/edit', views.CommentEditAPIView.as_view(), name='comment-update'),
]