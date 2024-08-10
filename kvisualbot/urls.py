from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import include, path

from kvisualbot.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1.0/", include("bot.urls")),
    path("api/health/", lambda r: HttpResponse(b"ok")),
    path("", index),
]
