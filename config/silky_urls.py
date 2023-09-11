"this file used with combination of django-silk package for local development"

from django.urls import include, path

from .urls import urlpatterns

urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
