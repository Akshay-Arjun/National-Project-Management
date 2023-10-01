from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from base.widgets import DateWidget, DurationWidget
from . import models
from base import custom_forms


class TaskForm(custom_forms.CustomModelForm):
    class Meta:
        model = models.Task
        fields = [
            "title",
            "description",
            "project",
            "priority_level",
            "estimated_duration",
            "date_due",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"autocomplete": "off"}),
            "description": forms.Textarea(attrs={"autocomplete": "off"}),
            "estimated_duration": DurationWidget(),
            "date_due": DateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.request_user

        if not user.profile.is_manager:
            q = user.profile.get_related_projects()
            self.fields["project"].queryset = q

    def clean_project(self):
        project = self.cleaned_data["project"]
        user = self.request_user

        if not user.profile.is_manager:
            if user not in project.team.members.all():
                msg = """You do not have permission to assign a task to a
                project that you are not a part of.
                """
                raise ValidationError(msg, code="Forbidden")

        return project


class AssignTaskForm(custom_forms.CustomModelForm):
    class Meta:
        model = models.Task
        fields = ["assigned_to"]


class CompleteTaskForm(custom_forms.CustomModelForm):
    class Meta:
        model = models.Task
        fields = [
            "date_completed",
        ]
        widgets = {"date_completed": DateWidget()}
