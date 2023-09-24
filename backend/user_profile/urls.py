from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('create/', views.ProfileCreateAPIView.as_view(), name='create-profile'),
    path('profiles_list/', views.ProfileListAPIView.as_view(), name='profile-list'),
    path('profile/<int:pk>/', views.ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateAPIView.as_view(), name="profile-edit"),
    path('profile/<int:pk>/delete/', views.ProfileDeleteAPIView.as_view(), name="profile-delete"),
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('login/', views.LoginUserAPIView.as_view(), name='login'),
    path('logout/', views.CustomLogoutAPIView.as_view(), name='logout'),
]