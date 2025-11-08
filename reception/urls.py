from django.urls import path
from reception import views
app_name = "reception"

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),

    path("course/list/", views.CourseListView.as_view(), name="course-list"),
    path("course/create/", views.CourseCreateView.as_view(), name="course-create"),
    path("courses/<int:pk>/groups/", views.CourseGroupListView.as_view(), name="course-groups"),
    path("course/<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("course/<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),


    path("group/list/", views.GroupListView.as_view(), name="group-list"),
    path("group/create/", views.GroupCreateView.as_view(), name="group-create"),
    path("groups/<int:pk>/students/", views.group_students, name="group-students"),
    path("group/<int:pk>/update/", views.GroupUpdateView.as_view(), name="group-update"),
    path("group/<int:pk>/delete/", views.GroupDeleteView.as_view(), name="group-delete"),


    path("student/list/", views.StudentListView.as_view(), name="student-list"),
    path("student/create/", views.StudentCreateView.as_view(), name="student-create"),
    path("student/<int:pk>/update/", views.StudentUpdateView.as_view(), name="student-update"),
    path("student/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student-delete"),


    path("lead/list/", views.LeadListView.as_view(), name="lead-list"),
    path("lead/create/", views.LeadCreateView.as_view(), name="lead-create"),
    path("lead/<int:pk>/update/", views.LeadUpdateView.as_view(), name="lead-update"),
    path("lead/<int:pk>/delete/", views.LeadDeleteView.as_view(), name="lead-delete"),

]
