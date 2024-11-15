from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from social_network.decorators.exception_decorators import catch_error
from social_network.utils.common_utils import print_log
from .. import services


class RequestOTPView(View):
    @catch_error
    def get(self, request):
        return render(request, "auth/request_otp.html")

    @catch_error
    def post(self, request):
        email = request.POST.get("email")
        next_url = request.GET.get("next", "/")

        # send otp to the email
        services.auth_service.send_otp(email)
        
        # take the user to verify otp page
        return render(
            request, f"auth/verify_otp.html", {"email": email, "next_url": next_url}
        )


class VerifyOTPView(View):
    @catch_error
    def post(self, request):
        email = request.POST.get("email")
        otp_code = request.POST.get("otp_code")

        # ger next page url
        next_url = request.POST.get("next", "/")

        if services.auth_service.verify_otp(email, otp_code):
            # get user by email
            user = services.user_service.get_user_by_email(email)

            # if user registered
            if user is not None:
                # login
                login(request, user)
                print_log("successfully logged in")
                
                # modify and save session
                request.session.modified = True
                request.session.save()

                # redirect to next page
                return redirect(next_url)
            
            # if user not registered
            else:
                return render(
                    request,
                    "auth/register.html",
                    {
                        "error": "User does not exist",
                        "email": email,
                        "next_url": next_url,
                    },
                )
        else:
            print_log("otp verification failed")
            return render(
                request,
                "auth/verify_otp.html",
                {
                    "error": "Invalid OTP or OTP expired",
                    "email": email,
                    "next_url": next_url,
                },
            )


class LogoutView(View):
    @catch_error
    def get(self, request):
        logout(request)
        return redirect("request_otp")


class UserRegistrationView(View):
    @catch_error
    def post(self, request):
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # get next page url
        next_url = request.POST.get("next_url", "/")

        # sign up
        user = services.auth_service.sign_up(first_name, last_name, email)

        # login
        login(request, user)
        print_log("successfully logged in")

        # modify and save session
        request.session.modified = True
        request.session.save()

        # redirect to next page
        return redirect(next_url)
