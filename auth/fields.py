from django import forms

from auth.settings import MINIMUM_PASSWORD_LENGTH, MAXIMUM_USERNAME_LENGTH


class UsernameField(forms.CharField):
    def __init__(self, **kwargs):
        super().__init__(max_length=MAXIMUM_USERNAME_LENGTH, **kwargs)


class PasswordField(forms.CharField):
    def __init__(self, **kwargs):
        super().__init__(
            min_length=MINIMUM_PASSWORD_LENGTH,
            widget=forms.PasswordInput(), **kwargs)
