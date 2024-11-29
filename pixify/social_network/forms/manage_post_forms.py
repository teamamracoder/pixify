from django import forms
from django.core.validators import URLValidator

from ..models.post_model import Post
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
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter post description", "rows": 2})
    )
    accessability = forms.ChoiceField(
        label="Accessibility",
        choices=[(1, "PUBLIC"), (2, "PRIVATE"), (3, "FRIENDS_ONLY")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    treat_as = forms.ChoiceField(
        label="Treat As",
        choices=[(type.value, type.name) for type in SpecificUserTreatment],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
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

    treat_as = forms.ChoiceField(
        label="Treat As",
        choices=[(type.value, type.name) for type in SpecificUserTreatment],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )


# class ManagePostSpecificUserCreateForm(forms.Form):
#     created_by = forms.CharField(
#         label="created_by",
#         required=False,
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter post description", "rows": 5})
#     )
#     post_id = forms.CharField(
#         label="post_id ",
#         required=False,
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter post description", "rows": 5})
#     )
#     specific_user_id = forms.CharField(
#         label="specific_user_id",
#         required=False,
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter post description", "rows": 5})
#     )