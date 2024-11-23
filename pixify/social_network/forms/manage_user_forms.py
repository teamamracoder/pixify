from django import forms
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    EmailValidator,
)

class ManageUserCreateForm(forms.Form):
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