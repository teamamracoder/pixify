from django import forms
# from .models import EndUserProfile 
from ..models import User 


from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    EmailValidator,
)


# badhan

# from .models import User
# from django.core.validators import RegexValidator
# 

# end

class ReqOtpForm(forms.Form):
    email = forms.EmailField(
        label="Please enter your email to continue",
        validators=[EmailValidator(message="Please enter valid email")],
        widget=forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
    )


class VerifyOtpForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.HiddenInput(),
    )
    otp = forms.CharField(
        label="Please enter OTP",
        min_length=6,
        max_length=6,
        validators=[
            MinLengthValidator(6, message="OTP must be minimum 6 characters long."),
            MaxLengthValidator(6, message="OTP must be maximum 6 characters long."),
        ],
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.HiddenInput(),
    )
    first_name = forms.CharField(
        label="First Name",
        min_length=3,
        max_length=15,
        validators=[
            MinLengthValidator(
                3, message="First Name must be minimum 3 characters long."
            ),
            MaxLengthValidator(
                15, message="First Name must be maximum 15 characters long."
            ),
        ],
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        min_length=3,
        max_length=15,
        validators=[
            MinLengthValidator(
                3, message="Last Name must be minimum 3 characters long."
            ),
            MaxLengthValidator(
                15, message="Last Name must be maximum 15 characters long."
            ),
        ],
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
    )










