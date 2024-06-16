from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

import json


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
            return None

        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None

        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return value
