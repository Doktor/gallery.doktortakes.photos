from django import forms
from django.contrib.auth import get_user_model

from photos.fields import PasswordField, UsernameField
from photos.utils import is_valid_username


class RegisterForm(forms.Form):
    username = UsernameField(
        help_text="Usernames can only contain "
                  "letters, numbers, and underscores.")
    email = forms.EmailField()
    password = PasswordField()
    password2 = PasswordField(label="Confirm password")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not is_valid_username(username):
            self.add_error(
                'username',
                forms.ValidationError(
                    "This username contains invalid characters."))

        if get_user_model().objects.filter(username__iexact=username).exists():
            self.add_error(
                'username',
                forms.ValidationError("This username is already in use."))

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if get_user_model().objects.filter(email__iexact=email).exists():
            self.add_error(
                'email',
                forms.ValidationError(
                    "This email is associated with an existing account."))

        return email

    def clean(self):
        data = super().clean()

        username = data.get('username', '')
        email = data.get('email', '')
        password = data.get('password', '')
        password2 = data.get('password2', '')

        if password != password2:
            self.add_error(
                'password',
                forms.ValidationError("The passwords don't match."))

        if password.lower() in (username.lower(), email.lower()):
            self.add_error(
                'password',
                forms.ValidationError(
                    "Your password can't be the same as your username/email."))
