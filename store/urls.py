from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'store'  # namespace added

urlpatterns = [
    path('', views.index, name='store-home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Products browsing
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),

    # Cart session management
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),  # Add this for checkout functionality


    # --- Product CRUD For Admin Panel ---
    path('admin/products/', views.admin_product_list, name='admin_product_list'),
    path('admin/products/add/', views.admin_add_product, name='admin_add_product'),
    path('admin/products/edit/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),
    path('admin/products/delete/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),

    # --- Order CRUD ---
    path('orders/', views.user_order_history, name='my_orders'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/edit/<int:order_id>/', views.admin_update_order, name='admin_update_order'),
    path('admin/orders/delete/<int:order_id>/', views.admin_delete_order, name='admin_delete_order'),

    # --- User Profile CRUD ---
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

]
