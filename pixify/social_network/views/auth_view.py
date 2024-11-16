from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from social_network.constants.default_values import ResponseMessageType
from social_network.packages.response import error_response, success_response
from social_network.constants.error_messages import ErrorMessage
from social_network.constants.success_messages import SuccessMessage
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

        # send otp to the email
        services.auth_service.send_otp(email)

        # take the user to verify otp page
        return render(
            request,
            f"auth/verify_otp.html",
            success_response(SuccessMessage.S000002.value, {"email": email}),
        )


class VerifyOTPView(View):
    @catch_error
    def post(self, request):
        email = request.POST.get("email")
        otp_code = request.POST.get("otp_code")

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

                # set message to session variable
                request.session["message"] = "Welcome to pixify"
                request.session["message_type"] = ResponseMessageType.SUCCESS.value
                # request.session.pop('temp_data', None)

                # redirect to next page
                return redirect("home")

            # if user not registered
            else:
                return render(
                    request,
                    "auth/register.html",
                    success_response(
                        SuccessMessage.S000003.value,
                        {"email": email},
                    ),
                )
        else:
            print_log("otp verification failed")
            return render(
                request,
                "auth/verify_otp.html",
                error_response(
                    ErrorMessage.E000004.value,
                    {"email": email},
                ),
            )


class LogoutView(View):
    @catch_error
    def get(self, request):
        logout(request)
        # set message to session variable
        request.session["message"] = SuccessMessage.S000004.value
        request.session["message_type"] = ResponseMessageType.INFO.value
        return redirect("request_otp")


class UserRegistrationView(View):
    @catch_error
    def post(self, request):
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # sign up
        user = services.auth_service.sign_up(first_name, last_name, email)

        # login
        login(request, user)
        print_log("successfully logged in")

        # modify and save session
        request.session.modified = True
        request.session.save()

        # set message to session variable
        request.session["message"] = "Welcome to pixify"
        request.session["message_type"] = ResponseMessageType.SUCCESS.value

        # redirect to next page
        return redirect("home")