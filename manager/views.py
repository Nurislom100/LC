from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from common import models, serializers
from manager import forms
from helpers.views import CreateView, UpdateView, DeleteView
from helpers.permissions import ManagerPassesTestMixin
from django.db.models import Q

class HomeView(ManagerPassesTestMixin,View):
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

class GroupDetailView(ListView):
    models = models.Group
    template_name = "manager/group/detail.html"
    context_object_name = "objects"
    
    def get_queryset(self):
        queryset = Model.models.objects.all()

        return queryset
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



class AttendanceView(View):
    def get(self, request, group_id):
        group = get_object_or_404(models.Group, id=group_id)
        return render(request, "manager/attendance/attendance.html", {"group": group})


class GroupStudentsAPIView(ListAPIView):
    serializer_class = serializers.StudentSerializer
    
    def get_queryset(self):
        return models.Student.objects.filter(group_id=self.kwargs['group_id']).only('id', 'full_name', 'date_joined')


class AttendanceListAPIView(ListAPIView):
    serializer_class = serializers.AttendanceSerializer
    def get_queryset(self):
        params = self.request.query_params
        filters = Q()
        
        if group_id := params.get('group'):
            filters &= Q(group_id=group_id)
        if start := parse_date(params.get('start_date', '')):
            filters &= Q(date_time__gte=start)
        if end := parse_date(params.get('end_date', '')):
            filters &= Q(date_time__lte=end)
        
        return models.Attendance.objects.filter(filters).only('id', 'student_id', 'date_time', 'is_present').order_by('date_time')


class SaveAttendanceAPIView(APIView):
    def post(self, request):
        attendance_list = request.data.get('attendance', [])
        
        if not attendance_list:
            return Response({'success': False})
        
        data_map = {}  
        student_ids = set()
        dates = set()
        
        for item in attendance_list:
            date_str = item.get('date_time', '').split('T')[0]
            if date_obj := parse_date(date_str):
                student_id = item['student']
                key = f"{student_id}-{date_obj}"
                data_map[key] = {
                    'student_id': student_id,
                    'group_id': item['group'],
                    'date': date_obj,
                    'is_present': item['is_present']
                }
                student_ids.add(student_id)
                dates.add(date_obj)
        
        existing = {
            f"{obj.student_id}-{obj.date_time}": obj
            for obj in models.Attendance.objects.filter(
                student_id__in=student_ids,
                date_time__in=dates
            )
        }
        
        to_create = []
        to_update = []
        
        for key, data in data_map.items():
            if key in existing:
                obj = existing[key]
                obj.is_present = data['is_present']
                to_update.append(obj)
            else:
                to_create.append(models.Attendance(
                    student_id=data['student_id'],
                    group_id=data['group_id'],
                    date_time=data['date'],
                    is_present=data['is_present']
                ))
        
        created = len(models.Attendance.objects.bulk_create(to_create, ignore_conflicts=True)) if to_create else 0
        updated = len(models.Attendance.objects.bulk_update(to_update, ['is_present'])) if to_update else 0
        
        return Response({
            'success': True,
            'created': created,
            'updated': updated
        })
