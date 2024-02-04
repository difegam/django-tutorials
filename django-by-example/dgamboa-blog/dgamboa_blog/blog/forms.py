from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """Form to share a post by email"""

    name = forms.CharField(max_length=25, label="Your name")
    email = forms.EmailField(label="Your email")
    to = forms.EmailField(label="Recipient email")
    comments = forms.CharField(required=False, widget=forms.Textarea, label="Comments")


class CommentForm(forms.ModelForm):
    """Form to create a comment"""

    class Meta:
        model = Comment
        fields = ("name", "email", "body")
        labels = (
            ("name", "Your name"),
            ("email", "Your email"),
            ("body", "Your comment"),
        )
