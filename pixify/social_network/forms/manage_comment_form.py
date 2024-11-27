from django import forms


class ManageCommentCreateForm(forms.Form):
    comment = forms.CharField(
        label="Comment",

        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    post_id=forms.CharField(
         label="Post_id",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
 


