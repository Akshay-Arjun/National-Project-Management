from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, mixins
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, reverse
from django.views import generic
import ast
from collections import Counter
from . import forms
from tasks.models import Task
from projects.models import Project
from teams.models import Team

class UserCreateView(SuccessMessageMixin, generic.CreateView):
    model = User
    form_class = forms.UserRegisterForm
    template_name = "users/user_register.html"
    success_message = "Your account was successfully created."

    def get_success_url(self):
        return reverse("dashboard")

    def form_valid(self, form):

        super().form_valid(form)
        user = self.object
        user.profile.roll_number = form.cleaned_data.get("roll_number")
        user.profile.college_name = form.cleaned_data.get("college_name")  
        user.profile.university_name = form.cleaned_data.get("university_name")  
        user.profile.save()
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return redirect(self.get_success_url())

class UserDetailView(
    mixins.LoginRequiredMixin, generic.DetailView,
):
    model = User
    template_name = "users/user_detail.html"
    slug_url_kwarg = "username"
    slug_field = "username"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.get_object().profile  # Retrieve the user's profile
        context["college_name"] = self.get_object().profile.college_name
        context["university_name"] = self.get_object().profile.university_name
        return context

class UserUpdateView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.UpdateView
):
    model = User
    form_class = forms.UserChangeForm
    template_name = "users/user_update.html"

    def get_object(self, queryset=None):
        user_pk = self.request.user.pk
        return User.objects.get(pk=user_pk)

    def get_success_url(self):
        return reverse("profile", args=[self.request.user.username])

    def test_func(self):
        return not self.request.user.profile.is_demo_user

class UserDeleteView(
    mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView
):
    model = User
    template_name = "users/user_confirm_delete.html"

    def get_object(self, queryset=None):
        user_pk = self.request.user.pk
        return User.objects.get(pk=user_pk)

    def get_success_url(self):
        return reverse("home")

    def test_func(self):
        return not self.request.user.profile.is_demo_user

def demo_user_login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=settings.DEMO_USER_USERNAME,
            password=settings.DEMO_USER_PASSWORD,
        )

        if user is not None:
            if user.profile.is_demo_user:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                msg = (
                    "The user you have provided is not a demo user. Please "
                    + "set a different demo user in your settings or change "
                    + "the current user to a demo user."
                )
                raise PermissionError(msg)

        messages.error(request, "Demo user account not setup, contact admin to setup a demo account")

    return render(request, template_name="users/login_demo_user.html")

class DashboardView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = "users/user_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all projects
        projects = Project.objects.all()
        #print(projects)
    # Extract and count technologies used
        technology_counts = Counter()
        project_completed_counts = 0
        project_active_counts = 0
    # Iterate through projects and count technologies
        for project in projects:
             technologies_used_str = project.technologies_used
             project_status = project.completed
             
             #print("Technologies used for project {}: {}".format(project.id, technologies_used))
             if technologies_used_str is not None:
                 #print(f"Technologies Used for project {project.id}: {technologies_used_str}") 
                 technologies_used_list = ast.literal_eval(technologies_used_str)
                 for tech in technologies_used_list:
                     technology_counts[tech] = technology_counts.get(tech, 0) + 1
             if project_status is not None:
                 if project_status:
                     project_completed_counts+=1
                 else:
                     project_active_counts+=1
                         
                    
        #print(project_completed_counts)
       # print(project_active_counts)
        #print(" project {}: {} {}".format(project.id, technologies_used_list, technology_counts))  
    # Prepare the data for the chart
        chart_labels =list(technology_counts.keys())

        chart_data = list(technology_counts.values())

        context["chart_labels"] = chart_labels
        context["chart_data"] = chart_data
        context["project_completed_counts"] = project_completed_counts
        context["project_active_counts"] = project_active_counts

        context["task_list"] = (
            Task.objects.filter(completed=False)
            .filter(assigned_to=self.request.user)
            .order_by("date_due", "-priority_level")[:7]
        )

        context["unassigned_task_list"] = (
            Task.objects.filter(completed=False)
            .filter(team__leader=self.request.user)
            .filter(assigned_to=None)
            .order_by("date_due", "-priority_level")[:7]
        )
        

        context["project_list"] = (
            Project.objects.filter(completed=False)
            .filter(team__members=self.request.user)
            .order_by("date_due")
        )

        context["team_list"] = Team.objects.filter(members=self.request.user)

        return context
