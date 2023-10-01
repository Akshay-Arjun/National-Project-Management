from django import forms
from . import models
from base import custom_forms


class TaskCommentForm(custom_forms.CustomModelForm):
    class Meta:
        model = models.TaskComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"cols": 80, "rows": 5, "autocomplete": "off"}
            )
        }


class ProjectCommentForm(custom_forms.CustomModelForm):
    class Meta:
        model = models.ProjectComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"cols": 80, "rows": 5, "autocomplete": "off"}
            )
        }
