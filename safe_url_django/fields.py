from django.db.models.fields import URLField
import validators
from django import oldforms

class Safe_URLField(URLField):
    def __init__(self, badware_check=True, **kwargs):
        if badware_check:
            kwargs.setdefault('validator_list', []).append(validators.isBadwareURL)
        self.badware_check = badware_check
        super(Safe_URLField, self).__init__(**kwargs)


    def get_manipulator_field_objs(self):
        return [oldforms.URLField]

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.URLField, 'verify_exists': self.verify_exists, }
        defaults.update(kwargs)
        return super(Safe_URLField, self).formfield(**defaults)
