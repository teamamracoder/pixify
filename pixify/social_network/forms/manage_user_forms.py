from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from ..models import User  # Import the User model

class ManageUserCreateForm(forms.ModelForm):
    """Form for creating a new user"""
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'dob', 'gender', 'address', 'relationship_status', 'hobbies']
        
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

    # Common field validators for the Create Form
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(50)
        ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your first name"})
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(50)
        ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your last name"})
    )

    email = forms.EmailField(
        validators=[EmailValidator(message="Please enter a valid email")],
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "abc123@gmail.com"})
    )


class ManageUserUpdateForm(forms.ModelForm):
    """Form for updating user data"""
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'dob', 'gender', 'address', 'relationship_status', 'hobbies']
        
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

    middle_name = forms.CharField(
        label="Middle Name",
        required=False,  # Middle name is optional
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your middle name"})
    )
