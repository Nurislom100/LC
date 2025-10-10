from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from common import models
from manager import forms
from helpers.views import CreateView, UpdateView, DeleteView
from helpers.permissions import ManagerPassesTestMixin


class HomeView(ManagerPassesTestMixin, View):
    def get(self, request):
        print(request.user.role)
        return render(request, "base/index.html")


class TeacherListView(ManagerPassesTestMixin, ListView):
    model = models.Teacher
    template_name = "manager/teacher/list.html"
    context_object_name = "objects"
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Teacher.objects.all().order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) | Q(surname__icontains=search)
            )
        return queryset

class TeacherCreateView(ManagerPassesTestMixin, CreateView):
    model = models.Teacher
    form_class = forms.TeacherForm
    template_name = "manager/teacher/create.html"
    context_object_name = "object"
    success_url = "manager:teacher-list"
    success_create_url = 'manager:teacher-create'
    
    
class TeacherUpdateView(ManagerPassesTestMixin, UpdateView):
    model = models.Teacher
    form_class = forms.TeacherForm
    template_name = "manager/teacher/update.html"
    context_object_name = "object"
    success_url = "manager:teacher-list"
    success_create_url = 'manager:teacher-update'
    

class TeacherDeleteView(ManagerPassesTestMixin, DeleteView):
    model = models.Teacher
    success_url = 'manager:teacher-list'
    
   

class CourseListView(ManagerPassesTestMixin, ListView):
    model = models.Course
    template_name = "manager/course/list.html"
    context_object_name = "courses"
    def get_queryset(self):
        queryset = models.Course.objects.all().order_by("id")
        search = self.request.GET.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
            )
        return queryset



class CourseCreateView(ManagerPassesTestMixin, CreateView):
    model = models.Course
    form_class = forms.CourseForm
    context_object_name = "object"
    template_name = "manager/course/create.html"
    success_url = "manager:course-list"
    success_create_url = "manager:course-list"


class CourseUpdateView(ManagerPassesTestMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    context_object_name = "object"
    template_name = "manager/course/update.html"
    success_url = "manager:course-list"
    success_update_url = "manager:course-update"


class CourseDeleteView(ManagerPassesTestMixin, DeleteView):
    model = models.Course
    success_url = "manager:course-list"


class GroupListView(ManagerPassesTestMixin, ListView):
    model = models.Group
    template_name = "manager/group/list.html"
    context_object_name = "objects"
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Group.objects.all().order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search))
        return queryset



class GroupCreateView(ManagerPassesTestMixin, CreateView):
    model = models.Group
    template_name = "manager/group/create.html"
    context_object_name = 'object'
    form_class = forms.GroupForm
    success_url = "manager:group-list"
    success_update_url = "manager:group-update"


class GroupUpdateView(ManagerPassesTestMixin, UpdateView):
    model = models.Group
    template_name = "manager/group/update.html"
    context_object_name = 'object'
    form_class = forms.GroupForm
    success_url = "manager:group-list"
    success_update_url = "manager:group-update"

class GroupDeleteView(ManagerPassesTestMixin, DeleteView):
    model = models.Group
    success_url = "manager:group-list"

class StudentListView(ManagerPassesTestMixin, ListView):
    model = models.Student
    template_name = "manager/student/list.html"
    context_object_name = "objects"
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Student.objects.all().order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(surname__icontains=search)
            )
        return queryset

class StudentCreateView(ManagerPassesTestMixin, CreateView):
    model = models.Student
    form_class = forms.StudentForm
    template_name = "manager/student/create.html"
    context_object_name = "object"
    success_url = "manager:student-list"
    success_create_url = 'manager:student-create'
    
    
class StudentUpdateView(ManagerPassesTestMixin, UpdateView):
    model = models.Student
    form_class = forms.StudentForm
    template_name = "manager/student/update.html"
    context_object_name = "object"
    success_url = "manager:student-list"
    success_create_url = 'manager:student-update'
    

class StudentDeleteView(ManagerPassesTestMixin, DeleteView):
    model = models.Student
    success_url = 'manager:student-list'



class BaseUserListView(ManagerPassesTestMixin, ListView):
    model = models.BaseUser
    template_name = "manager/user/list.html"
    context_object_name = "objects"
    queryset = models.BaseUser.objects.all().order_by("-id")
    paginate_by = 10


class BaseUserCreateView(ManagerPassesTestMixin, CreateView):
    model = models.BaseUser
    form_class = forms.BaseUserForm
    template_name = "manager/user/create.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_create_url = "manager:user-create"


class BaseUserUpdateView(ManagerPassesTestMixin, UpdateView):
    model = models.BaseUser
    form_class = forms.BaseUserForm
    template_name = "manager/user/update.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_create_url = "manager:user-update"


class BaseUserDeleteView(ManagerPassesTestMixin, DeleteView):
    model = models.BaseUser
    success_url = 'manager:user-list'
    
