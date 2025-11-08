from django import forms
from helpers import widgets as widget
from common import models
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'role', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_1'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Password fieldlarni chiroyli qilish
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}
        )

        # Manager rolini chiqarib tashlash
        if 'role' in self.fields:
            self.fields['role'].choices = [
                (value, label) for value, label in self.fields['role'].choices
                if label != 'Manager'
            ]


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
            "group",
            "phone",
            "address",
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
            "balance" : forms.TextInput(attrs={"class" : "form-control", "placeholder": "balance"}),
            "date_joined": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status" : forms.Select(attrs={"class" : "form-control", "id": "kt_select2_2"}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.Payment
        fields = [
            'student',
            'group',
            'amount',
            'date',
        ]
        widgets = {
            'student' : forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_2"}),
            "group": forms.Select(attrs={"class" : "form-control", "id" : "kt_select2_2"}), 
            'amount' : forms.NumberInput(attrs={"class" : "form-control", }),
            'date' : forms.DateInput(attrs={"class" : "form-control", "type" : "date"})
        }

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
        fields = ['Name', 'capacity']
        widgets = {
            'Name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Xona nomini kiriting (masalan: 1-xona)'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sig‘imi (masalan: 20 o‘quvchi)'
            }),
        }
        labels = {
            'Name': 'Xona nomi',
            'capacity': 'Sig‘imi',
        }