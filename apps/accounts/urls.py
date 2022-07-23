from accounts.views import UserCreateView
from django.urls import include, path

urlpatterns = [path("", include("django.contrib.auth.urls")), path("signup/", UserCreateView.as_view(), name="signup")]
