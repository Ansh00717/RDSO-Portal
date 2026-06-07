from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class RegistrationForm(forms.Form):
    """
    Registration form with first name, last name, email, and captcha.
    Password is NOT collected — it is auto-generated server-side and emailed.
    """
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'reg-first-name',
            'class': 'textbox',
            'autocomplete': 'given-name',
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'reg-last-name',
            'class': 'textbox',
            'autocomplete': 'family-name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'reg-email',
            'class': 'textbox',
            'autocomplete': 'email',
        })
    )
    captcha = CaptchaField()

    def clean_email(self):
        """Check that the email is not already registered."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(forms.Form):
    """
    Login form with email and password fields.
    Authentication is handled in the view, not the form.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'login-email',
            'class': 'textbox',
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'login-pass',
            'class': 'textbox',
        })
    )