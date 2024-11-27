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
    )# forms.py
from django import forms
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    EmailValidator,
)

from ..models import User  # Import your User model

class ManageUserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'dob',
            'gender',
            'address',
            'relationship_status',
            'hobbies',
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your first name"}),
            'middle_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your middle name"}),
            'last_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your last name"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "abc123@gmail.com"}),
            'dob': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            'address': forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter Address", "rows": 2}),
            'hobbies': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter hobbies (comma-separated)"}),
        }

        labels = {
            'first_name': "First Name",
            'middle_name': "Middle Name",
            'last_name': "Last Name",
            'email': "Email",
            'dob': "Date of Birth",
            'gender': "Gender",
            'address': "Address",
            'relationship_status': "Relationship Status",
            'hobbies': "Hobbies",
        }


class ManageUserUpdateForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        validators=[
            MinLengthValidator(2, message="First name must be at least 2 characters."),
            MaxLengthValidator(50, message="First name should be at most 50 characters.")
        ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your first name"})
    )
    
    middle_name = forms.CharField(
        label="Middle Name",
        required=False,  # Middle name is optional
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your middle name"})
    )

    last_name = forms.CharField(
        label="Last Name",
        validators=[
            MinLengthValidator(2, message="Last name must be at least 2 characters."),
            MaxLengthValidator(50, message="Last name should be at most 50 characters.")
        ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your last name"})
    )
    
    email = forms.EmailField(
        label="Email",
        validators=[EmailValidator(message="Please enter a valid email")],
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "abc123@gmail.com"})
    )
