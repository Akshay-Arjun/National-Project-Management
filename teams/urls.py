from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TeamListView.as_view(), name="teams"),
    path("create/", views.TeamCreateView.as_view(), name="create-team"),
    path("team/<int:pk>/", views.TeamDetailView.as_view(), name="team-detail"),
    path(
        "team/<int:pk>/update/",
        views.TeamUpdateView.as_view(),
        name="team-update",
    ),
    path(
        "team/<int:pk>/delete/",
        views.TeamDeleteView.as_view(),
        name="team-delete",
    ),
]
