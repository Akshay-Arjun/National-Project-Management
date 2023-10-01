from datetime import timedelta

from django import forms


class DateWidget(forms.TextInput):
    input_type = "date"


class DurationWidget(forms.MultiWidget):
    template_name = "base/widgets/duration_widget.html"

    def __init__(self, attrs=None):
        HOUR_MIN = 0
        HOUR_MAX = 23
        MINUTE_MIN = 0
        MINUTE_MAX = 59
        hour_attrs = {
            "min": HOUR_MIN,
            "max": HOUR_MAX,
            "placeholder": "hh",
            "class": "form-control",
        }
        minute_attrs = {
            "min": MINUTE_MIN,
            "max": MINUTE_MAX,
            "placeholder": "mm",
            "class": "form-control",
        }
        if attrs:
            hour_attrs.update(attrs)
            minute_attrs.update(attrs)

        widgets = [
            forms.NumberInput(attrs=hour_attrs),
            forms.NumberInput(attrs=minute_attrs),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, timedelta):
            return [value.hours, value.minutes]

        elif isinstance(value, str):
            hours, minutes, _ = value.split(":")
            return [hours, minutes]

        return [None, None]

    def value_from_datadict(self, data, files, name):
        hours, minutes = super().value_from_datadict(data, files, name)
        return f"{hours}:{minutes}:00"
