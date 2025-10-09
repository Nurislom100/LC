from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from common import models
from manager import forms
from helpers.views import CreateView, UpdateView, DeleteView

class HomeView(View):
    def get(self, request):
        print(request.user.role)
        return render(request, "base/index.html")


class TeacherListView(ListView):
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

class TeacherCreateView(CreateView):
    model = models.Teacher
    form_class = forms.TeacherForm
    template_name = "manager/teacher/create.html"
    context_object_name = "object"
    success_url = "manager:teacher-list"
    success_create_url = 'manager:teacher-create'
    
    
class TeacherUpdateView(UpdateView):
    model = models.Teacher
    form_class = forms.TeacherForm
    template_name = "manager/teacher/update.html"
    context_object_name = "object"
    success_url = "manager:teacher-list"
    success_create_url = 'manager:teacher-update'
    

class TeacherDeleteView(DeleteView):
    model = models.Teacher
    success_url = 'manager:teacher-list'
    
   

class CourseListView(ListView):
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



class CourseCreateView(CreateView):
    model = models.Course
    form_class = forms.CourseForm
    context_object_name = "object"
    template_name = "manager/course/create.html"
    success_url = "manager:course-list"
    success_create_url = "manager:course-list"


class CourseUpdateView(UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    context_object_name = "object"
    template_name = "manager/course/update.html"
    success_url = "manager:course-list"
    success_update_url = "manager:course-update"


class CourseDeleteView(DeleteView):
    model = models.Course
    success_url = "manager:course-list"


class GroupListView(ListView):
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



class GroupCreateView(CreateView):
    model = models.Group
    template_name = "manager/group/create.html"
    context_object_name = 'object'
    form_class = forms.GroupForm
    success_url = "manager:group-list"
    success_update_url = "manager:group-update"


class GroupUpdateView(UpdateView):
    model = models.Group
    template_name = "manager/group/update.html"
    context_object_name = 'object'
    form_class = forms.GroupForm
    success_url = "manager:group-list"
    success_update_url = "manager:group-update"

class GroupDeleteView(DeleteView):
    model = models.Group
    success_url = "manager:group-list"

class StudentListView(ListView):
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

class StudentCreateView(CreateView):
    model = models.Student
    form_class = forms.StudentForm
    template_name = "manager/student/create.html"
    context_object_name = "object"
    success_url = "manager:student-list"
    success_create_url = 'manager:student-create'
    
    
class StudentUpdateView(UpdateView):
    model = models.Student
    form_class = forms.StudentForm
    template_name = "manager/student/update.html"
    context_object_name = "object"
    success_url = "manager:student-list"
    success_create_url = 'manager:student-update'
    

class StudentDeleteView(DeleteView):
    model = models.Student
    success_url = 'manager:student-list'



class BaseUserListView(ListView):
    model = models.BaseUser
    template_name = "base/user/list.html"
    context_object_name = "objects"
    queryset = models.BaseUser.objects.all().order_by("-id")
    paginate_by = 10


class BaseUserCreateView(CreateView):
    model = models.BaseUser
    form_class = forms.BaseUserForm
    template_name = "base/user/create.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_create_url = "manager:user-create"


class BaseUserUpdateView(UpdateView):
    model = models.BaseUser
    form_class = forms.BaseUserForm
    template_name = "base/user/update.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_create_url = "manager:user-update"
