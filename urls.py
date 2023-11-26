from django.urls import path
from . import views
from .views import dlt_variant  # Import the dlt_variant function

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/<int:user_id>/', views.dlt_user, name='dlt_user'),
    path('users/<int:user_id>/', views.edit_user, name='edit_user'),
    path('category/', views.admin_category, name='admin_category'),
    path('category/<int:cid>/', views.dlt_category, name='dlt_category'),
    path('brand/', views.admin_brand, name='admin_brand'),
    path('brand/<int:bid>/', views.dlt_brand, name='dlt_brand'),
    path('products/', views.admin_products, name='admin_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('admin_coupon/', views.admin_coupon, name='admin_coupon'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('add_product/<int:pid>/', views.add_product, name='edit_product'),
    path('add_variant/', views.add_variant, name='add_variant'),
    path('edit_variant/<int:pv_id>/', views.edit_variant, name='edit_variant'),
    path('update_status/<int:order_item_id>', views.update_status, name='update_status'),
    # path('add_variant/<int:pid>/', views.add_variant, name='edit_variant'),
    path('admin_product/<int:product_id>/', views.dlt_product, name='dlt_product'),
    path('admin_product/<int:product_id>/product-listing/', views.product_listing, name='product_listing'),
    # path('admin_variant/<int:pv_id>/', dlt_variant, name='dlt_variant'),
    path('variants/', views.admin_variant, name='admin_variant'),
    path('variants/<int:pv_id>/toggle-listing/', views.toggle_listing, name='toggle_listing'),
    path('admin_category/<int:category_id>/unlist_category/', views.unlist_category, name='unlist_category'),
    path('admin_brand/<int:brand_id>/unlist_brand/', views.unlist_brand, name='unlist_brand'),
    path('logout/',views.logout_view,name='admin_logout'),
]
