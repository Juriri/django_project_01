from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .cb_views import SignupView, LoginView, verify_email

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path("verify/", verify_email, name="verify_email"),
]
