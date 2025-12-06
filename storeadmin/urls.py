from django.urls import path
from . import views

app_name = "storeadmin"

urlpatterns = [
    # Auth
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Products CRUD
    path('products/', views.admin_products, name='admin_products'),
    path('products/add/', views.admin_add_product, name='admin_add_product'),
    path('products/edit/<int:id>/', views.admin_edit_product, name='admin_edit_product'),
    path('products/delete/<int:id>/', views.admin_delete_product, name='admin_delete_product'),

    # Orders CRUD
    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/<int:id>/', views.admin_order_detail, name='admin_order_detail'),
    path('orders/update/<int:id>/', views.admin_update_order_status, name='admin_update_order_status'),
    path('orders/delete/<int:id>/', views.admin_delete_order, name='admin_delete_order'),
]
