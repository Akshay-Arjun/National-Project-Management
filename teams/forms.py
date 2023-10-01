from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from . import models
from base import custom_forms

class TeamForm(forms.ModelForm):
    class Meta:
        model = models.Team
        fields = ["name", "leader", "members"]
        widgets = {"name": forms.TextInput(attrs={"autocomplete": "off"})}

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        if request_user:
            # Exclude users with profile.is_demo_user & superuser aka admin set to True from the leader and members queryset
            self.fields["leader"].queryset = User.objects.exclude(profile__is_demo_user=True).exclude(is_superuser=True)
            self.fields["members"].queryset = User.objects.exclude(profile__is_demo_user=True).exclude(is_superuser=True)
        #self.fields["members"].widget = forms.CheckboxSelectMultiple(attrs={'class': 'multi-column'}) #uncomment for checkboxes 

    def clean(self):
        cleaned_data = super().clean()
        leader = cleaned_data.get("leader")
        members = cleaned_data.get("members")

        if leader and members:
            if leader not in members.all():
                msg = f"The team leader must be included as a member of the team."
                self.add_error("leader", msg)

        return cleaned_data