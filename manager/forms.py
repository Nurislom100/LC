from django import forms
from helpers import widgets as widget
from common import models

class BaseUserForm(forms.ModelForm):
    class Meta:
        model = models.BaseUser
        fields = [
            "full_name",
            "username",
            "phone",
            "role",
            "teacher_profile",
            "password",
        ]
        widgets = {
            "full_name" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Full name"}),
            "username" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Username"}),
            "phone" : forms.TelInput(attrs={"class" : "form-control", "placeholder" : "Phone"}),
            "role" : forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_2"}),
            "teacher_profile" : forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_3"}),
            "password" : forms.PasswordInput(attrs={"class" : "form-control", "placeholder" : "Password"})
        }


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
            "price",
            "description",
        ]
        widgets = {
            "title" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Title"}),
            "duration" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Duration"}),
            "address" : forms.TextInput(attrs={"class" : "form-control", "id" : "address"}),
            "price" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Price"}),
            "description" : forms.Textarea(attrs={"class" : "form-control", "placeholder": "description"})
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = [
            "title",
            "course",
            "teacher",
            "lesson_days",
            "time",
            'date_started',
            'status'

        ]
        widgets = {
            "title" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Title"}),
            "course" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),
            "teacher" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),
            "lesson_days" : forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_2"}),
            "time" : forms.TimeInput(attrs={"class" : "form-control", "placeholder" : "Time"}),
            "date_started" : widget.DateWidget(attrs={"class" : "form-control", "id": "kt_datetimepicker_3"}),
            "status" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"})
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = [
            "full_name",
            "birth_date",
            "phone",
            "address",
            "balance",
            "date_joined",
            "status",
        ]
        widgets = {
            "full_name" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Full name"}),
            "birth_date" : widget.DateWidget(attrs={"class" : "form-control", "id": "kt_datetimepicker_3"}),
            "phone" : forms.TelInput(attrs={"class" : "form-control", "placeholder" : "Phone"}),
            "address" : forms.TextInput(attrs={"class" : "form-control", "placeholder" : "Address"}),
            "balance" : forms.TextInput(attrs={"class" : "form-control", "placeholder": "balance"}),
            "date_joined" : widget.DateWidget(attrs={"class" : "form-control", "id": "kt_datetimepicker_3"}),

        }


