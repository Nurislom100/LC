from django.urls import path

from manager import views

app_name = "manager"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    #user
    path("user/list/", views.BaseUserListView.as_view(), name="user-list"),
    path("user/create/", views.BaseUserCreateView.as_view(), name="user-create"),
    path("user/<int:pk>/update/", views.BaseUserUpdateView.as_view(), name="user-create")

]
