from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User


class BlockDemoUserMixin:
    """Stops demo users from submitting a form."""

    def clean(self):

        try:
            self.request_user
        except AttributeError as err:
            msg = (
                "Using the BlockDemoUserMixin requires the parent form to "
                + "have an attribute 'request_user' representing the user who "
                + "is requesting the form."
            )

            raise AttributeError(msg) from err

        if self.request_user.profile.is_demo_user:
            msg = """Demo users cannot create or update objects."""
            code = "Forbidden"

            raise ValidationError(msg, code=code)

        return super().clean()


class CustomForm(BlockDemoUserMixin, forms.Form):
    """Django form that blocks demo users from submitting it. Note: requires a
    keyword argument 'user' that is the user requesting the form.
    """

    def __init__(self, *args, **kwargs):
        try:
            user = kwargs.pop("user")
        except KeyError as err:
            msg = (
                "CustomForm requires a key word argument 'user' who is "
                + "the user requesting the form."
            )
            raise ValueError(msg) from err

        if not isinstance(user, User):
            msg = "The user argument must be an instance of the User class."
            raise TypeError(msg)

        self.request_user = user
        super().__init__(*args, **kwargs)


class CustomModelForm(BlockDemoUserMixin, forms.ModelForm):
    """Django model form that blocks demo users from submitting it. Note:
    requires a keyword argument 'user' that is the user requesting the form.
    """

    def __init__(self, *args, **kwargs):
        try:
            user = kwargs.pop("user")
        except KeyError as err:
            msg = (
                "CustomModelForm requires a key word argument 'user' who is "
                + "the user requesting the form."
            )
            raise ValueError(msg) from err

        if not isinstance(user, User):
            msg = "The user argument must be an instance of the User class."
            raise TypeError(msg)

        self.request_user = user
        super().__init__(*args, **kwargs)
