
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("posts", views.posts_view, name="posts"),
    path("posts/<int:post_id>", views.post_view, name="post"),
    path("posts/<user_name>", views.userposts_view, name="userposts"),
	path("users/<user_name>", views.user_view, name="user"),
	path("following", views.following_view, name="following")
]
