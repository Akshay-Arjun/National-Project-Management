from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    roll_number = forms.CharField(max_length=50, required=False)
    college_name = forms.CharField(max_length=100, required=True, label="College Name")
    university_name = forms.CharField(max_length=100, required=False, label="University Name")
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "college_name",
            "university_name",
            "roll_number",
            "email",
            "password1",
            "password2",  
        ]


from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import User

class UserChangeForm(BaseUserChangeForm):
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput,
        required=False,  # Password is not required for profile update
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        required=False,  # Password is not required for profile update
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("The new passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password1 = self.cleaned_data.get("new_password1")
        if new_password1:
            user.set_password(new_password1)

        if commit:
            user.save()
        return user
