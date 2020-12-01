from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
	path("admin_products", views.admin_products, name="admin_products"),
	path("admin_products/edit_product/<product_id>", views.edit_product, name="edit_product"),
	path("admin_products/<product_id>", views.delete_product, name="delete_product"),
    path("cart", views.cart, name="cart"),
	path("orders", views.orders, name="orders")
]