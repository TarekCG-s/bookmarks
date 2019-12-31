from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "username"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "password"}
        )
    )


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    agreement = forms.BooleanField(
        widget=forms.CheckboxInput,
        label="I Agree to the terms and conditions of using this website.",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

    def clean_password1(self):
        password1 = self.cleaned_data["password1"]
        if len(password1) < 8:
            raise forms.ValidationError("Password must be longer than 8 characters.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2
