
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/articles/', include('articles.urls')),
    path('api/user/', include('user_profile.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
