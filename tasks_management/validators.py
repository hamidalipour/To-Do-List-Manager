import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_date(value):
    if value < datetime.date.today():
        raise ValidationError(
            _("the date should be in the future"),
            params={"value": value},
        )
