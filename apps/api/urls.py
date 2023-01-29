"""
Versioned API url.
"""
from django.conf.urls import include
from django.urls import path

from .v1.routes import get_router_urls as get_v1_router_urls

urlpatterns = [
    path("v1/", include(get_v1_router_urls())),
]
