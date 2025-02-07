from django import forms
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
   )

class ManagMessageCreateForm(forms.Form):
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
    chat_id = forms.CharField(
        label="Chat_ID",      
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    