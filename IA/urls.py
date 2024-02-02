from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('ranking/', views.home, name='ranking'),
    path('generate/', views.generate_image, name='generate_image'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/filter_all/', views.filter_cards_by_category, {'category': 'all'}, name='inventory_all'),
    path('inventory/filter_weapon/', views.filter_cards_by_category, {'category': 'Weapons'}, name='filter_weapons'),
    path('inventory/filter_potion/', views.filter_cards_by_category, {'category': 'Potions'}, name='filter_potions'),
    path('inventory/filter_armor/', views.filter_cards_by_category, {'category': 'Armors'}, name='filter_armors'),
]
