from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from tasks import models as task_models
from projects import models as project_models
from . import forms


class PostTaskComment(
    SuccessMessageMixin, generic.detail.SingleObjectMixin, generic.FormView
):
    template_name = "tasks/task_detail.html"
    form_class = forms.TaskCommentForm
    model = task_models.Task
    success_message = "You're comment was added successfully."

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task = self.object
        if form.is_valid():
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("task-detail", kwargs={"pk": self.object.pk})


class PostProjectComment(
    SuccessMessageMixin, generic.detail.SingleObjectMixin, generic.FormView
):
    template_name = "projects/project_detail.html"
    form_class = forms.ProjectCommentForm
    model = project_models.Project
    success_message = "You're comment was added successfully."

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.project = self.object
        if form.is_valid():
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project-detail", kwargs={"pk": self.object.pk})
