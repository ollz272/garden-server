from django.urls import include, path

from accounts.views import UserCreateView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", UserCreateView.as_view(), name="signup")
]
