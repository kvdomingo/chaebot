from django.contrib import admin
from django.urls import include, path

from kvisualbot.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1.0/", include("bot.urls")),
    path("/", index),
]
