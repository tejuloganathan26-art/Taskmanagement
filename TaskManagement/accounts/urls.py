from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Register
    path("register/", views.register, name="register"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),

    # Login
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

     path("dashboard/", views.dashboard, name="dashboard"),   # ✅ Must exist

    # Forgot Password
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-reset-otp/", views.verify_reset_otp, name="verify_reset_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
    
]
