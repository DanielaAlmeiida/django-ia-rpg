from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('generate/', views.generate_image, name='generate_image'),
    path('inventory/', views.inventory, name='inventory'),
]
