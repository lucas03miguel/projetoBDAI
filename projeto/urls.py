from django.contrib import admin
from app import views
from django.urls import path, include  

urlpatterns = [
    path('', views.login, name='login'), 
    path('admin', admin.site.urls),  # URL do admin
    path('app/', include('app.urls')),  # Inclui as URLs do seu aplicativo
]
