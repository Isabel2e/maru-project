

from django.contrib import admin
from django.urls import path
from comentario.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", UserListView.as_view(), name="user-list"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/register/", register_user, name="register_user"),
    path("api/login/", login_view, name="login"),
    path("api/users/me/", CurrentUserView.as_view(), name="current_user"),
    path("api/csrf-token/", csrf_token_view, name="csrf_token"),
    path("api/register-word/", registerWord, name="register_word"),
    path("api/user/<str:username>/", UserDetailView.as_view(), name="user-detail"),
]
