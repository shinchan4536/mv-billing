from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='billing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('paint/', views.paint_pos, name='paint_pos'),
    path('electrical/', views.electrical_pos, name='electrical_pos'),
    path('paint/checkout/', views.paint_checkout, name='paint_checkout'),
    path('paint/history/', views.paint_history, name='paint_history'),
    path('paint/receipt/<int:invoice_id>/', views.paint_receipt, name='paint_receipt'),
    path('electrical/', views.electrical_pos, name='electrical_pos'),
    path('electrical/checkout/', views.electrical_checkout, name='electrical_checkout'),
    path('electrical/history/', views.electrical_history, name='electrical_history'),
    path('electrical/receipt/<int:invoice_id>/', views.electrical_receipt, name='electrical_receipt'),
    path('inventory/add/', views.add_product, name='add_product'),
    path('inventory/manage/', views.manage_inventory, name='manage_inventory'),
    path('inventory/update/', views.update_inventory_item, name='update_inventory_item'),
]