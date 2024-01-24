from django.contrib import admin
from django.urls import path, include
from IA import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.generateImage, name='index'),
]
