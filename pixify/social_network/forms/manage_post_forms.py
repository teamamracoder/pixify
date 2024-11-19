from django import forms
from django.core.validators import URLValidator
from  ..import models
from ..constants.default_values import PostType, SpecificUserTreatment
from ..models.user_model import User

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

class ManagePostCreateForm(forms.Form):
    posted_by = forms.CharField(
        label="Posted By",
        # validators=[
        #     MinLengthValidator(2, message="Name must be at least 2 characters."),
        #     MaxLengthValidator(50, message="Name should be at most 50 characters.")
        # ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the name of the user who posted"})
    )
    type = forms.ChoiceField(
        label="Post Type",
        choices=[(1, "NORMAL"), (2, "FEATURED"), (3, "PROMOTED")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    content_type = forms.ChoiceField(
        label="Content Type",
        choices=[(1, "TEXT"), (2, "IMAGE"), (3, "VIDEO")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    # media_url = forms.CharField(
    #     label="Media URLs",
    #     required=False,
    #     validators=[URLValidator(message="Please enter valid URLs.")],
    #     widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter media URLs separated by commas", "rows": 3})
    # )
    title = forms.CharField(
        label="Title",
        required=False,
        validators=[
            MaxLengthValidator(50, message="Title should not exceed 50 characters.")
        ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter post title"})
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter post description", "rows": 5})
    )
    accessability = forms.ChoiceField(
        label="Accessibility",
        choices=[(1, "PUBLIC"), (2, "PRIVATE"), (3, "FRIENDS_ONLY")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    # members = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"})
    # )
    # tags = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"})
    # )
    treat_as = forms.ChoiceField(
        label="Treat As",
        choices=[(type.value, type.name) for type in SpecificUserTreatment],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    # is_active = forms.BooleanField(
    #     label="Is Active",
    #     required=False,
    #     widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    # )
    # created_by = forms.ModelChoiceField(
    #     queryset=User.objects.all(),
    #     required=True,
    #     widget=forms.Select(attrs={"class": "form-control"})
    # )
    # updated_by = forms.ModelChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     widget=forms.Select(attrs={"class": "form-control"})
    # )
    # created_at = forms.DateTimeField(
    #     label="Created At",
    #     widget=forms.DateTimeInput(attrs={"class": "form-control", "readonly": "readonly"}),
    #     required=False
    # )
    # updated_at = forms.DateTimeField(
    #     label="Updated At",
    #     widget=forms.DateTimeInput(attrs={"class": "form-control", "readonly": "readonly"}),
    #     required=False
    # )







class ManagePostUpdateForm(forms.Form):
    posted_by = forms.CharField(
        label="Posted By",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter the name of the user who posted"})
    )
    type = forms.ChoiceField(
        label="Post Type",
        choices=[(1, "NORMAL"), (2, "FEATURED"), (3, "PROMOTED")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    content_type = forms.ChoiceField(
        label="Content Type",
        choices=[(1, "TEXT"), (2, "IMAGE"), (3, "VIDEO")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    # media_url = forms.CharField(
    #     label="Media URLs",
    #     required=False,
    #     validators=[URLValidator(message="Please enter valid URLs.")],
    #     widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter media URLs separated by commas", "rows": 3})
    # )
    title = forms.CharField(
        label="Title",
        required=False,
        validators=[
            MaxLengthValidator(50, message="Title should not exceed 50 characters.")
        ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter post title"})
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter post description", "rows": 5})
    )
    accessability = forms.ChoiceField(
        label="Accessibility",
        choices=[(1, "PUBLIC"), (2, "PRIVATE"), (3, "FRIENDS_ONLY")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    # members = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"})
    # )
    # tags = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"})
    # )
    treat_as = forms.ChoiceField(
        label="Treat As",
        choices=[(type.value, type.name) for type in SpecificUserTreatment],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    # is_active = forms.BooleanField(
    #     label="Is Active",
    #     required=False,
    #     widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    # )
    # created_by = forms.ModelChoiceField(
    #     queryset=User.objects.all(),
    #     required=True,
    #     widget=forms.Select(attrs={"class": "form-control"})
    # )
    # updated_by = forms.ModelChoiceField(
    #     queryset=User.objects.all(),
    #     required=False,
    #     widget=forms.Select(attrs={"class": "form-control"})
    # )
    # created_at = forms.DateTimeField(
    #     label="Created At",
    #     widget=forms.DateTimeInput(attrs={"class": "form-control", "readonly": "readonly"}),
    #     required=False
    # )
    # updated_at = forms.DateTimeField(
    #     label="Updated At",
    #     widget=forms.DateTimeInput(attrs={"class": "form-control", "readonly": "readonly"}),
    #     required=False
    # )