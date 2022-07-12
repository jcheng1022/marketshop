from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('items/browse/', views.item_index, name='index'),
    path('items/<int:item_id>', views.items_detail, name ="item_detail"),
    path('accounts/signup/', views.signup, name='signup'),
    path('items/create', views.ItemCreate.as_view(), name='items_create'),
    path('items/<int:pk>/update/', views.ItemUpdate.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', views.ItemDelete.as_view(), name='item_delete'),
]