from django.urls import path, include
from manager import views

app_name = "manager"

urlpatterns = [
    path("api/attendance/", views.AttendanceListAPIView.as_view(), name="attendance-list"),
    path("api/attendance/save/", views.SaveAttendanceAPIView.as_view(), name="save-attendance"),
    path("attendance/<int:group_id>/", views.AttendanceView.as_view(), name="attendance-page"),
    path("api/groups/<int:group_id>/students/", views.GroupStudentsAPIView.as_view(), name="group-students"),
    path("", views.HomeView.as_view(), name='home'),
    path("user/list/", views.BaseUserListView.as_view(), name="user-list"),
    path("user/create/", views.BaseUserCreateView.as_view(), name="user-create"),
    path("user/<int:pk>/update/", views.BaseUserUpdateView.as_view(), name="user-update"),
    path("user/<int:pk>/delete/", views.BaseUserDeleteView.as_view(), name="user-delete"),


    path("teacher/list/", views.TeacherListView.as_view(), name="teacher-list"),
    path("teacher/create/", views.TeacherCreateView.as_view(), name="teacher-create"),
    path("teacher/<int:pk>/update/", views.TeacherUpdateView.as_view(), name="teacher-update"),
    path("teacher/<int:pk>/delete/", views.TeacherDeleteView.as_view(), name="teacher-delete"),



    path("course/list/", views.CourseListView.as_view(), name="course-list"),
    path("course/create/", views.CourseCreateView.as_view(), name="course-create"),
    path("course/<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("course/<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),


    path("group/list/", views.GroupListView.as_view(), name="group-list"),
    path("group/create/", views.GroupCreateView.as_view(), name="group-create"),
    path("group/<int:pk>/update/", views.GroupUpdateView.as_view(), name="group-update"),
    path("group/<int:pk>/delete/", views.GroupDeleteView.as_view(), name="group-delete"),
    path("group/<int:pk>/detail/", views.GroupDetailView.as_view(), name="group-detail"),

    path("student/list/", views.StudentListView.as_view(), name="student-list"),
    path("student/create/", views.StudentCreateView.as_view(), name="student-create"),
    path("student/<int:pk>/update/", views.StudentUpdateView.as_view(), name="student-update"),
    path("student/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student-delete")


]
