from django import forms
from helpers import widgets as widget
from common import models
from common.models import Student
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = models.BaseUser
        fields = ['username', 'email', 'role', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_1'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            "phone" : forms.TelInput(attrs={"class" : "form-control", "placeholder" : "Phone"}),
            "role" : forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_2"}),
            "teacher_profile" : forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_3"}),
            "password" : forms.PasswordInput(attrs={"class" : "form-control", "placeholder" : "Password"})


        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        if commit:
            user.save()
        return user


class TeacherForm(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = [
            "full_name",
            "birth_date",
            "phone",
            "address",
            "status",
        ]
        widgets = {
            "full_name" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Full name"}),
            "birth_date" : widget.DateWidget(attrs={"class" : "form-control", "id": "kt_datetimepicker_3"}),
            "phone" : forms.TelInput(attrs={"class" : "form-control", "placeholder" : "Phone"}),
            "address" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Address"}),
            "status" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),

            }

class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = [
            "title",
            "duration",
            "description",
        ]
        widgets = {
            "title" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Title"}),
            "duration" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Duration"}),
            "address" : forms.TextInput(attrs={"class" : "form-control", "id" : "address"}),
            "description" : forms.Textarea(attrs={"class" : "form-control", "placeholder": "description"})
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = [
            "title",
            "course",
            "room",
            "teacher",
            'start_time',
            'end_time',
            "price",
            "lesson_days",
            'date_started',
            'status'

        ]
        widgets = {
            "title" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Title"}),
            "course" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),
            "teacher" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),
            "room" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),
            "start_time" : forms.TimeInput(attrs={"class" : "form-control", "placeholder" : "Time"}),
            "end_time" : forms.TimeInput(attrs={"class" : "form-control", "placeholder" : "Time"}),
            "lesson_days" : forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_2"}),
            "date_started" : widget.DateWidget(attrs={"class" : "form-control", "id": "kt_datetimepicker_3"}),
            "status" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),
            "price" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Price"}),

        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = [
            "full_name",
            "birth_date",
            "group",
            "phone",
            "address",
            "group",
            "balance",
            "date_joined",
            "status",
        ]
        widgets = {
            "full_name" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Full name"}),
            "birth_date" : widget.DateWidget(attrs={"class" : "form-control", "id": "kt_datetimepicker_3"}),
            "group": forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_2"}), 
            "phone" : forms.TelInput(attrs={"class" : "form-control", "placeholder" : "Phone"}),
            "address" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Address"}),
            "group" : forms.Select(attrs={"class" : "form-control", "placeholder" : "group", "id": "kt_select2_2"}),
            "balance" : forms.TextInput(attrs={"class" : "form-control", "placeholder": "balance"}),
            "date_joined": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),
            "date_joined" : widget.DateWidget(attrs={"class" : "form-control", "id": "kt_datetimepicker_2"}),
            
        }



class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.Payment
        fields = ['group', 'student', 'amount', 'date']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control selectpicker','data-live-search': 'true','id': 'id_group'}),
            'student': forms.Select(attrs={'class': 'form-control selectpicker','data-live-search': 'true','id': 'id_student'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Enter amount'}),
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Boshlang'ichda student queryset bo‘sh bo‘lsin
        self.fields['student'].queryset = Student.objects.none()

        # POST so‘rov bo‘lsa yoki update
        if 'group' in self.data:
            try:
                group_id = int(self.data.get('group'))
                self.fields['student'].queryset = Student.objects.filter(group_id=group_id)
            except (ValueError, TypeError):
                self.fields['student'].queryset = Student.objects.none()
        elif self.instance and self.instance.pk:
            self.fields['student'].queryset = Student.objects.filter(group=self.instance.group)

class LeadForm(forms.ModelForm):
    class Meta:
        model = models.Lead
        fields = [
            "full_name",
            "birth_date",
            "phone",
            "interested_course",
            "address",
            "status",
        ]
        widgets = {
            "full_name" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Full name"}),
            "birth_date" : widget.DateWidget(attrs={"class" : "form-control", "id": "kt_datetimepicker_3"}),
            "interested_course" : forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_2"}),
            "phone" : forms.TelInput(attrs={"class" : "form-control", "placeholder" : "Phone"}),
            "address" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Address"}),
            "status" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"})
        }

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = models.Classroom
        fields = ['name', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }

