from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="all-tasks"),
    path("active/", views.ActiveTaskListView.as_view(), name="active-tasks"),
    path(
        "completed/",
        views.CompletedTaskListView.as_view(),
        name="completed-tasks",
    ),
    path(
        "unassigned/",
        views.UnassignedTaskListView.as_view(),
        name="unassigned-tasks",
    ),
    path("create/", views.TaskCreateView.as_view(), name="create-task"),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path(
        "task/<int:pk>/update/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "task/<int:pk>/assign/",
        views.TaskAssignView.as_view(),
        name="task-assign",
    ),
    path(
        "task/<int:pk>/assign-to-self/",
        views.TaskAssignToSelfView.as_view(),
        name="task-assign-to-self",
    ),
    path(
        "task/<int:pk>/complete/",
        views.TaskCompleteView.as_view(),
        name="task-complete",
    ),
    path(
        "task/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
]
