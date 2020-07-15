from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("search_results/<str:query>", views.search_results, name="search_results"),
    path("create", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
	path("random_entry", views.random_entry, name="random_entry"),
	path("error", views.error, name="error")
]
