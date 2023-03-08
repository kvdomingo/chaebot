from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import status


def index(_):
    return HttpResponseRedirect(settings.WEBAPP_URL, status=status.HTTP_307_TEMPORARY_REDIRECT)
