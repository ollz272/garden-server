from django.urls import path

from plants import views

urlpatterns = [
    path(r'chart', views.plants),
]
