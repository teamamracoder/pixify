from django import forms
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
   
)

# CREATE_CHAT
# ===============================================
class ManageChatCreateForm(forms.Form):
    title = forms.CharField(
        label="Title",
        validators=[
            MinLengthValidator(3, message="Title name must be at least 3 characters."),
            MaxLengthValidator(20, message="Title name should be at most 20 characters.")
        ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your title name"})
    )
    
    type = forms.IntegerField(
        label="Type",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    chat_cover = forms.URLField(
        label="Chat_Cover",
        validators=[MinLengthValidator(1, message="Chat_Cover must be at least 1 characters."),
            MaxLengthValidator(400, message="Chat_Cover should be at most 400 characters.")],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Text in Chat cover"})
    )


# UPDATE_CHAT
# ===========================================
class ManageChatUpdateForm(forms.Form):
    title = forms.CharField(
        label="Title",
        validators=[
            MinLengthValidator(3, message="Title name must be at least 3 characters."),
            MaxLengthValidator(20, message="Title name should be at most 20 characters.")
        ],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your title name"})
    )
    
    type = forms.IntegerField(
        label="Type",
        widget=forms.TextInput(attrs={"class": "form-control"})
)
    
    chat_cover = forms.URLField(
        label="Caht_Cover",
        validators=[MinLengthValidator(1, message="Chat_Cover must be at least 1 characters."),
            MaxLengthValidator(400, message="Chat_Cover should be at most 400 characters.")],
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Text in Chat cover"})
    )

    # Add fields for middle_name, dob, address, etc. as needed...


# Manage_Member_Chat
# ===========================================
class ManageMemberChatCreateForm(forms.Form):
    member_id_id = forms.CharField(
        label="Member_Id",       
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter User Id"})
    )   
    chat_id_id = forms.CharField(
        label="Chat_Id",
        widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Enter Chat Id"})
        )