from django.shortcuts import render ,get_object_or_404
from django.views import View
from django.views.generic import ListView , DeleteView
from django.urls import reverse_lazy   
from django.db.models import Q 
from common import models
from manager import forms
from common.models import Group,Course,Teacher,Student
from helpers.views import CreateView, UpdateView, DeleteView
from common import mixins
from django.views.generic import TemplateView, ListView, View
from datetime import date ,datetime
import calendar
from django.utils.timezone import now
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from common.models import Attendance , Student ,Grade
from common.serializers import AttendanceSerializer , StudentSerializer
from common import serializers



class ManagerHomeView(mixins.RoleRequiredMixin, TemplateView):
    template_name = "manager/base/index.html"
    allowed_roles = ['manager']


class Settings(ListView):
    template_name = "manager/settings/list.html"
    model = Group
    context_object_name = "groups"  # template-da shu nom bilan ishlatamiz

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Group.objects.filter(id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # bitta group obyektini template-da alohida olish uchun
        context['group'] = self.get_queryset().first()
        context['active_tab'] = 'all'  # All tab faollash
        return context
    
def student_monthly_stats(request, group_id):
    year = int(request.GET.get('year', now().year))
    month = int(request.GET.get('month', now().month))

    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, 28) + datetime.timedelta(days=4)
    end_date = end_date - datetime.timedelta(days=end_date.day)

    # Active qo'shilganlar
    new_added = Student.objects.filter(
        group_id=group_id,
        date_joined__range=[start_date, end_date],
        status="Active"
    ).count()

    # Archive bo'lganlar shu oy qo'shilganlar va status="Archive"
    archived = Student.objects.filter(
        group_id=group_id,
        date_joined__range=[start_date, end_date],
        status="Archive"
    ).count()

    return JsonResponse({
        "new_added": new_added,
        "archived": archived,
    })



class TeacherListView(ListView):
    model = models.Teacher
    template_name = "manager/teacher/list.html"
    context_object_name = "objects"
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Teacher.objects.filter(status="Active").order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search)
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
                Q(title__icontains=search)
            )
        return queryset

class CourseGroupListView(ListView):
    model = Group
    template_name = "manager/course/course_groups.html"
    context_object_name = "groups"

    def get_queryset(self):
        course_id = self.kwargs["pk"]
        return Group.objects.filter(course_id=course_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = Course.objects.get(pk=self.kwargs["pk"])
        return context

class CourseCreateView(CreateView):
    model = models.Course
    form_class = forms.CourseForm
    context_object_name = "object"
    template_name = "manager/course/create.html"
    success_url ="manager:course-list"
    success_create_url ="manager:course-list"


class CourseUpdateView(UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    context_object_name = "object"
    template_name = "manager/course/update.html"
    success_url = "manager:course-list"
    success_update_url = "manager:course-update"


class CourseDeleteView(DeleteView):
    model = models.Course
    success_url ="manager:course-list"


class GroupListView(ListView):
    model = models.Group
    template_name = "manager/group/list.html"
    context_object_name = "objects"
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Group.objects.filter(status="Active").order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search))
        return queryset

def group_students(request, pk):
    group = get_object_or_404(Group, pk=pk)
    students = group.students.filter() 
    context = {
        "group":group,
        "students":students,
    }
    return render(request, "manager/group/group_students.html",context)

class GroupfilterView(ListView):
    model = Group
    template_name = "manager/group/list.html"
    context_object_name = "objects"

    def get_queryset(self):
        queryset = Group.objects.all()
        filter_value = self.request.GET.get("filter", "all")

        if filter_value == "mwf":
            queryset = queryset.filter(lesson_days__icontains="Mon Wed Fri")
        elif filter_value == "tts":
            queryset = queryset.filter(lesson_days__icontains="Tu Thu Sat")
        # else -> all

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

class GroupCreateView(CreateView):
    model = models.Group
    template_name = "manager/group/create.html"
    context_object_name = 'object'
    form_class = forms.GroupForm
    success_url ="manager:group-list"
    success_update_url ="manager:group-update" 


class GroupUpdateView(UpdateView):
    model = models.Group
    template_name = "manager/group/update.html"
    context_object_name = 'object'
    form_class = forms.GroupForm
    success_url ="manager:group-list"
    success_update_url ="manager:group-update"

class GroupDeleteView(DeleteView):
    model = models.Group
    success_url ="manager:group-list"

class StudentListView(ListView):
    model = models.Student
    template_name = "manager/student/list.html"
    context_object_name = "objects"
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Student.objects.filter(status="Active").order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search)
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
    success_url ="manager:student-list"
    success_create_url = 'manager:student-update'
    

class StudentDeleteView(DeleteView):
    model = models.Student
    success_url ='manager:student-list'




class UserListView(ListView):
    model = models.User
    template_name = "manager/user/list.html"
    context_object_name = "objects"  # template'da objects ishlatiladi

    paginate_by = 10


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # formga request yuboramiz
        return kwargs

class UserCreateView(CreateView):
    model = models.User
    form_class = forms.UserForm
    template_name = "manager/user/create.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_create_url = "manager:user-create"


class UserUpdateView(UpdateView):
    model = models.User
    form_class = forms.UserForm
    template_name = "manager/user/update.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_update_url = "manager:user-update"


class UserDeleteView(DeleteView):
    model = models.User
    success_url = "manager:user-list"

   


class PaymentListView(ListView):
    model = models.Payment
    template_name = "manager/payment/list.html"
    context_object_name = "objects" 
    paginate_by = 10

    def get_queryset(self):
        queryset = models.Payment.objects.all().order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(id__icontains=search) 
            )
        return queryset

class PaymentCreateView(CreateView):
    model = models.Payment
    template_name = "manager/payment/create.html"
    context_object_name = 'object'
    form_class = forms.PaymentForm
    success_url = "manager:payment-list"
    success_update_url = "manager:payment-update"

class PaymentUpdateView(UpdateView):
    model = models.Payment
    template_name = "manager/payment/create.html"
    context_object_name = 'object'
    form_class = forms.PaymentForm
    success_url = "manager:payment-list"
    success_update_url = "manager:payment-update"

class PaymentDeleteView(DeleteView):
    model = models.Payment
    success_url = "manager:payment-list"

class PaymentDetailView(DeleteView):
    model = models.Payment
    template_name = "manager/payment-create.html"

    def get_queryset(self):
        queryset = models.Payment.objects.all()
        return queryset
    

class LeadListView(ListView):
    model = models.Lead
    template_name = "manager/lead/list.html"
    context_object_name = "objects"
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Lead.objects.all().order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(surname__icontains=search)
            )
        return queryset

class LeadCreateView(CreateView):
    model = models.Lead
    form_class = forms.LeadForm
    template_name = "manager/lead/create.html"
    context_object_name = "object"
    success_url = "manager:lead-list"
    success_create_url = 'manager:lead-create'
    
    
class LeadUpdateView(UpdateView):
    model = models.Lead
    form_class = forms.LeadForm
    template_name = "manager/lead/update.html"
    context_object_name = "object"
    success_url ="manager:lead-list"
    success_create_url = 'manager:lead-update'
    

class LeadDeleteView(DeleteView):
    model = models.Lead
    success_url ='manager:lead-list'

class ClassroomListView(ListView):
    model = models.Classroom
    template_name = "manager/classroom/list.html"
    context_object_name = "objects"
    paginate_by = 10
    def get_queryset(self):
        queryset = models.Classroom.objects.filter().order_by("id")
        search = self.request.GET.get("search", None)
        
        if search:
            queryset = queryset.filter(
                Q(Name__icontains=search)
            )
        return queryset

class ClassroomCreateView(CreateView):
    model = models.Classroom
    form_class = forms.ClassroomForm
    template_name = "manager/classroom/create.html"
    context_object_name = "object"
    success_url = "manager:classroom-list"
    success_create_url = 'manager:classroom-create'
    
    
class ClassroomUpdateView(UpdateView):
    model = models.Classroom
    form_class = forms.ClassroomForm
    template_name = "manager/classroom/update.html"
    context_object_name = "object"
    success_url = "manager:classroom-list"
    success_create_url = 'manager:classroom-update'
    

class ClassroomDeleteView(DeleteView):
    model = models.Classroom
    success_url = 'manager:classroom-list'
    



def Archive_list_view(request):
    context = {
        "archive_teachers": Teacher.objects.filter(status="Archive"),
        "archive_students": Student.objects.filter(status="Archive"),
        "groups_finished": Group.objects.filter(status="Finished"),
    }
    return render(request, "manager/archived/list.html", context)
    



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
    

class GradeView(View):
    def get(self, request, group_id):
        group = get_object_or_404(models.Group, id=group_id)
        return render(request, "manager/Rating/rating.html", {"group": group})


class GroupStudentsAPIView(ListAPIView):
    serializer_class = serializers.StudentSerializer
    
    def get_queryset(self):
        return models.Student.objects.filter(
            group_id=self.kwargs['group_id']
        ).only('id', 'full_name', 'date_joined')


class GradeListAPIView(ListAPIView):
    serializer_class = serializers.GradeSerializer
    
    def get_queryset(self):
        params = self.request.query_params
        filters = Q()
        
        if group_id := params.get('group'):
            filters &= Q(group_id=group_id)
        if start := parse_date(params.get('start_date', '')):
            filters &= Q(date_time__gte=start)
        if end := parse_date(params.get('end_date', '')):
            filters &= Q(date_time__lte=end)
        if subject_id := params.get('subject'):
            filters &= Q(subject_id=subject_id)
        
        return models.Grade.objects.filter(filters).select_related(
            'student', 'subject'
        ).only(
            'id', 'student_id', 'subject_id', 'date_time', 'grade', 'comment'
        ).order_by('date_time')


class SaveGradeAPIView(APIView):
    def post(self, request):
        grade_list = request.data.get('grades', [])
        
        if not grade_list:
            return Response({'success': False, 'error': 'No grades provided'})
        
        data_map = {}
        student_ids = set()
        dates = set()
        
        for item in grade_list:
            date_str = item.get('date_time', '').split('T')[0]
            if date_obj := parse_date(date_str):
                student_id = item['student']
                subject_id = item.get('subject')
                key = f"{student_id}-{subject_id}-{date_obj}"
                
                data_map[key] = {
                    'student_id': student_id,
                    'group_id': item['group'],
                    'subject_id': subject_id,
                    'date': date_obj,
                    'grade': item['grade'],
                    'comment': item.get('comment', '')
                }
                student_ids.add(student_id)
                dates.add(date_obj)
        
        # Mavjud baholarni topish
        existing = {
            f"{obj.student_id}-{obj.subject_id}-{obj.date_time}": obj
            for obj in models.Grade.objects.filter(
                student_id__in=student_ids,
                date_time__in=dates
            )
        }
        
        to_create = []
        to_update = []
        
        for key, data in data_map.items():
            if key in existing:
                obj = existing[key]
                obj.grade = data['grade']
                obj.comment = data['comment']
                to_update.append(obj)
            else:
                to_create.append(models.Grade(
                    student_id=data['student_id'],
                    group_id=data['group_id'],
                    subject_id=data['subject_id'],
                    date_time=data['date'],
                    grade=data['grade'],
                    comment=data['comment']
                ))
        
        created = len(models.Grade.objects.bulk_create(
            to_create, ignore_conflicts=True
        )) if to_create else 0
        
        updated = len(models.Grade.objects.bulk_update(
            to_update, ['grade', 'comment']
        )) if to_update else 0
        
        return Response({
            'success': True,
            'created': created,
            'updated': updated
        })