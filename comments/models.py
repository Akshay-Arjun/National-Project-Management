from django.db import models
from tasks.models import Task
from django.contrib.auth.models import User
from projects.models import Project


class TaskComment(models.Model):

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(verbose_name="comment")

    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task comment #{self.id}"


class ProjectComment(models.Model):

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(verbose_name="comment")

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Project comment #{self.id}"
