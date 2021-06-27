from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

import json

from photos.settings_photos import MAXIMUM_USERNAME_LENGTH, MINIMUM_PASSWORD_LENGTH


class JSONWidget(widgets.Textarea):
    template_name = 'widgets/json.html'

    def render(self, name, value, **kwargs):
        context = {
            'name': name,
            'data': json.dumps(value),
        }

        return mark_safe(render_to_string(self.template_name, context))


class JSONField(models.TextField):
    widget = JSONWidget

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None

        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return value


class UsernameField(forms.CharField):
    def __init__(self, **kwargs):
        super().__init__(max_length=MAXIMUM_USERNAME_LENGTH, **kwargs)


class PasswordField(forms.CharField):
    def __init__(self, **kwargs):
        super().__init__(
            min_length=MINIMUM_PASSWORD_LENGTH,
            widget=forms.PasswordInput(), **kwargs)