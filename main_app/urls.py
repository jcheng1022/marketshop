from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('items/browse/', views.item_index, name='index'),
]