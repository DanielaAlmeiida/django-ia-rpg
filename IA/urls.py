from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ranking/', views.ranking, {'category': 'all'}, name='ranking'),
    path('ranking/filter_all/', views.ranking, {'category': 'all'}, name='filter_all'),
    path('ranking/filter_weapon/', views.ranking, {'category': 'Weapons'}, name='filter_weapons'),
    path('ranking/filter_potion/', views.ranking, {'category': 'Potions'}, name='filter_potions'),
    path('ranking/filter_armor/', views.ranking, {'category': 'Armors'}, name='filter_armors'),
    path('generate/', views.generate_image, name='generate_image'),
    path('inventory/', views.inventory, {'category': 'all'}, name='inventory'),
    path('inventory/filter_all/', views.inventory, {'category': 'all'}, name='filter_all'),
    path('inventory/filter_weapon/', views.inventory, {'category': 'Weapons'}, name='filter_weapons'),
    path('inventory/filter_potion/', views.inventory, {'category': 'Potions'}, name='filter_potions'),
    path('inventory/filter_armor/', views.inventory, {'category': 'Armors'}, name='filter_armors'),
]