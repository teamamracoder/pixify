from django import forms
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
   )

class ManageNotificationCreateForm(forms.Form):
    text = forms.CharField(
        label="Text",
        validators=[
            MinLengthValidator(2, message="Text at least 20 characters."),
            MaxLengthValidator(50, message="Text at least 60 characters.")
        ],
        widget=forms.TextInput(attrs={"class": "form-control"})
    )  
    media_url = forms.URLField(
        label="Media_URL",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    receiver_id = forms.CharField(
        label="Receiver_ID",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )    


class ManageNotificationUpdateForm(forms.Form):
    text = forms.CharField(
        label="text",
        validators=[
            MinLengthValidator(2, message="Text at least 20 characters."),
            MaxLengthValidator(50, message="Text at least 60 characters.")
        ],
        widget=forms.TextInput(attrs={"class": "form-control"})
    )    
    media_url = forms.URLField(
        label="media_url",  
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    receiver_id = forms.CharField(
        label="Receiver_ID",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )