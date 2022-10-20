from accounts.views import UserCreateView, UserLoginView
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    # Login and logout
    path("login/", UserLoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),
    path("signup/", UserCreateView.as_view(), name="signup"),
]
