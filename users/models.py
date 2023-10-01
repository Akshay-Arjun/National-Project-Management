from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    college_name = models.CharField(max_length=100, blank=True, null=True)
    university_name = models.CharField(max_length=100, blank=True, null=True)
    is_manager = models.BooleanField(default=False)
    is_demo_user = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_connections(self):
        """A queryset of users who share a team with the user object."""
        q = User.objects.filter(pk=self.user.pk)
        for team in self.user.team_set.all():
            q = q | team.members.all()
        return q.distinct()

    def get_related_projects(self):
        q = Project.objects.none()
        for team in self.user.team_set.all():
            q = q | team.project_set.all()
        return q.distinct()
