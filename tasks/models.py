from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from projects.models import Project
from teams.models import Team
from datetime import date


class Task(models.Model):
    PRIORITY_LEVELS = [
        (3, "Low"),
        (6, "Medium"),
        (9, "High"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Assign to",
    )

    priority_level = models.IntegerField(choices=PRIORITY_LEVELS, default=3)
    estimated_duration = models.DurationField(help_text="hh:mm")

    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_tasks",
    )  # Set to current user on form validation
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="modified_tasks",
    )  # Set to current user on form validation
    date_due = models.DateField(help_text="dd/mm/yyyy")

    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)
    completed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="completed_tasks",
    )  # Set to current user on form validation

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})

    @property
    def days_till_due(self):
        difference = self.date_due - date.today()
        return difference.days

    # Model validation
    def clean(self):

        if hasattr(self, "project"):
            self.team = self.project.team

        if self.assigned_to and self.assigned_to not in self.team.members.all():
            msg = """The user who this task is assigned to must be part of
                    the project's team.
                """
            raise ValidationError(msg)

    # Authorization tests
    def team_has_member(self, user):
        return user in self.team.members.all()

    def team_leader_is(self, user):
        return user == self.team.leader

    def is_assigned_to(self, user):
        return user == self.assigned_to

    def was_created_by(self, user):
        return user == self.created_by
