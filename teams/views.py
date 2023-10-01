from datetime import date
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views import View, generic
from .forms import TeamForm
from comments import forms as comment_forms
from comments import views as comment_views
from django.views.generic import CreateView
from . import forms
from .models import Team
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User  # Import User model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView



class TeamListView(mixins.LoginRequiredMixin, generic.ListView):
    """Shows a list of all users teams"""

    model = Team

    def get_queryset(self):
        user = self.request.user
        q1 = Team.objects.filter(members=user)
        q2 = Team.objects.filter(created_by=user)

        return q1.union(q2)


class TeamDetailView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DetailView,
):
    model = Team

    def test_func(self):
        team = self.get_object()
        user = self.request.user

        if user.profile.is_manager:
            return True
        if team.was_created_by(user):
            return True
        return team.has_member(user)


class TeamCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Team
    form_class = TeamForm
    success_message = "Team {name} was created successfully"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Exclude users with profile.is_demo_user & superuser aka admin set to True from the leader and members queryset
        form.fields["leader"].queryset = User.objects.exclude(profile__is_demo_user=True).exclude(is_superuser=True)
        form.fields["members"].queryset = User.objects.exclude(profile__is_demo_user=True).exclude(is_superuser=True)
      
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
    def get_success_message(self, cleaned_data):
        return self.success_message.format(name=cleaned_data.get("name"))

class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Team
    form_class = TeamForm
    success_message = "Team {name} was updated successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        return self.success_message.format(name=cleaned_data.get("name"))

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        team = self.get_object()
        user = self.request.user

        if team.was_created_by(user):
            return True
        return team.leader_is(user)

class TeamDeleteView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView,
):
    model = Team
    success_url = "/teams"

    def test_func(self):
        team = self.get_object()
        user = self.request.user

        if user.profile.is_demo_user:
            return False
        if team.was_created_by(user):
            return True
        return team.leader_is(user)
