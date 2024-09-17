from django.urls import path
from . import views

app_name = 'seller'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_products/', views.view_products, name='view_products'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
]