from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bookmarks/", include("bookmark.urls")),
    # path("todo/", include("todolist.urls")),
    path("cbv/", include("todolist.urls")),
    # path("accounts/", include("users.urls")),
    path("users/", include("users.urls")),
    path("summernote/", include("django_summernote.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
