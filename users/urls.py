from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("register/", views.UserCreateView.as_view(), name="register"),
    path(
        "view/<str:username>/", views.UserDetailView.as_view(), name="profile"
    ),
    path("update/", views.UserUpdateView.as_view(), name="profile-update"),
    path("delete/", views.UserDeleteView.as_view(), name="profile-delete"),
    path(
        "login/demo-user/", views.demo_user_login_view, name="demo-user-login"
    ),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        html_email_template_name='users/password_reset_email.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
