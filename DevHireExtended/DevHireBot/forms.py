from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, validate_file_size
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={"class": "px-2 my-1", "placeholder": "Locus"}
        ),
        required=True,  # Set the field as required
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={"class": "px-2 my-1", "placeholder": "Focus"}
        ),
        required=True,  # Set the field as required
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom classes to the widget attributes for each field
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "px-2 my-1"

        self.fields["username"].widget.attrs["placeholder"] = "LocusFocus"
        self.fields["email"].widget.attrs["placeholder"] = "locusfocus@gmail.com"
        self.fields["password1"].widget.attrs["placeholder"] = "abc123"
        self.fields["password2"].widget.attrs[
            "placeholder"
        ] = "abc123 (again)"



    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

class ResumeForm(forms.Form):
    resume = forms.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size
        ]
    )