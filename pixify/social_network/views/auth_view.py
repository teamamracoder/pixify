# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from social_network.utils.common_utils import print_log
from .. import services


class RequestOTPView(View):
    def get(self, request):
        return render(request, "auth/request_otp.html")

    def post(self, request):
        email = request.POST.get("email")
        next_url = request.GET.get("next", "/")
        try:
            user = services.user_service.get_user_by_email(email)
            services.auth_service.send_otp(user)
            return render(
                request, f"auth/verify_otp.html", {"email": email, "next_url": next_url}
            )
        except Exception as e:
            print_log(e)
            return render(
                request, "auth/request_otp.html", {"error": "User does not exist"}
            )


class VerifyOTPView(View):
    def post(self, request):
        email = request.POST.get("email")
        otp_code = request.POST.get("otp_code")
        next_url = request.POST.get("next", "/")
        try:
            user = services.user_service.get_user_by_email(email)
            if services.auth_service.verify_otp(user, otp_code):
                # login
                login(request, user)
                print_log("successfully logged in")
                # modify and save session
                request.session.modified = True
                request.session.save()
                # redirect to next page
                return redirect(next_url)
            else:
                print_log("login failed")
                return render(
                    request,
                    "auth/verify_otp.html",
                    {
                        "error": "Invalid OTP or OTP expired",
                        "email": email,
                        "next_url": next_url,
                    },
                )
        except Exception as e:
            print_log(e)
            return render(
                request, "auth/request_otp.html", {"error": "User does not exist"}
            )


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("request_otp")
