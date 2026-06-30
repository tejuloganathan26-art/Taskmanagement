from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
import random

User = get_user_model()


# ---------------- HOME ----------------

def home(request):
    return render(request, "accounts/home.html")


# ---------------- REGISTER ----------------

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == "POST":
        

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Username already exists"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {
                "error": "Email already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect("login")

    return render(request, "accounts/register.html")


# ---------------- VERIFY OTP ----------------

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def verify_otp(request):

    if request.method == "POST":

        otp = request.POST.get("otp")

        if otp == request.session.get("otp"):

            User.objects.create_user(
                username=request.session["username"],
                email=request.session["email"],
                password=request.session["password"]
            )

            request.session.flush()

            return redirect("login")

        return render(request, "accounts/verify_otp.html", {
            "error": "Invalid OTP"
        })

    return render(request, "accounts/verify_otp.html")

# ---------------- FORGOT PASSWORD ----------------

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        # Check whether email exists
        try:
           user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "accounts/forgot_password.html", {
                "error": "Email not found"
            })

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP and Email in session
        request.session["reset_email"] = email
        request.session["reset_otp"] = otp

        # Send OTP Email
        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP is: {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect("verify_reset_otp")

    return render(request, "accounts/forgot_password.html")


# ---------------- VERIFY RESET OTP ----------------

def verify_reset_otp(request):

    if request.method == "POST":

        otp = request.POST.get("otp")

        if otp == request.session.get("reset_otp"):
            return redirect("reset_password")

        return render(request, "accounts/verify_otp.html", {
            "error": "Invalid OTP"
        })

    return render(request, "accounts/verify_otp.html")


# ---------------- RESET PASSWORD ----------------

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()

def reset_password(request):

    if request.method == "POST":

        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            return render(request, "accounts/reset_password.html", {
                "error": "Passwords do not match"
            })

        email = request.session.get("reset_email")

        user = User.objects.get(email=email)
        user.password = make_password(password)
        user.save()

        request.session.flush()

        return redirect("login")

    return render(request, "accounts/reset_password.html")


# ---------------- CHANGE PASSWORD ----------------

def change_password(request):
    return render(request, "accounts/change_password.html")

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")   # Go to dashboard

        return render(request, "accounts/login.html", {
            "error": "Invalid Username or Password"
        })

    return render(request, "accounts/login.html")

from django.contrib.auth import logout
from django.shortcuts import redirect
def logout_view(request):
    logout(request)
    return redirect("login")

from django.shortcuts import render

def dashboard(request):
    return render(request, "accounts/dashboard.html")