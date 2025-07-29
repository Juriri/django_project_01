from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bookmarks/", include("bookmark.urls")),
    path("todo/", include("todolist.urls")),
    path("accounts/", include("users.urls")),
]
