from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="all-projects"),
    path(
        "active/", views.ActiveProjectListView.as_view(), name="active-projects"
    ),
    path(
        "completed/",
        views.CompletedProjectListView.as_view(),
        name="completed-projects",
    ),
    path("create/", views.ProjectCreateView.as_view(), name="create-project"),
    path(
        "project/<int:pk>/",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "project/<int:pk>/update/",
        views.ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "project/<int:pk>/complete/",
        views.ProjectCompleteView.as_view(),
        name="project-complete",
    ),
    path(
        "project/<int:pk>/delete/",
        views.ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path(
        "project/<int:pk>/addtask/",
        views.ProjectAddTaskView.as_view(),
        name="project-add-task",
    ),
]
