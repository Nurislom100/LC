from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from helpers.models import BaseModel


class BaseUser(AbstractUser):
    role_choices = [
        ("manager", "Manager"),
        ("reception", "Reception"),
        ("accountant", "Accountant"),
        ("teacher", "teacher"),
    ]
    full_name = models.CharField(_("full name"), max_length=256, null=True, blank=True)
    username = models.CharField(_("username"), max_length=256, unique=True)
    phone = models.CharField(_("phone"), max_length=256, null=True)
    role = models.CharField(_("role"), max_length=256, choices=role_choices, null=True)
    teacher_profile = models.ForeignKey("common.Teacher", on_delete=models.CASCADE, verbose_name="teacher profile", related_name="users", null=True, blank=True)
    password = models.CharField(_("password"), max_length=256)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username


class Teacher(BaseModel):
    status_choices = [
        ("active", "ACTIVE"),
        ("archived", "ARCHIVED")
    ]
    full_name = models.CharField(_("full name"), max_length=256)
    birth_date = models.DateField(_("birth date"))
    phone = models.CharField(_("phone"), max_length=256)
    address = models.CharField(_("address"), max_length=256)
    status = models.CharField(_("status"), max_length=256, choices=status_choices)

    class Meta:
        db_table = "teachers"
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")

    def __str__(self):
        return self.full_name

class Course(BaseModel):
    title = models.CharField(_("title"), max_length=256)
    description = models.TextField(_("description"), null=True, blank=True)
    duration = models.CharField(_("duration"), max_length=256)
    price = models.IntegerField(_("price"))

    class Meta:
        db_table = "courses"
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.title


class Group(BaseModel):
    day_choices = [
        ("mo we fri","Mo We Fri"),
        ("tu thu sa","Tu Thu Sa"),
    ]
    status_choices = [
        ("active", "ACTIVE"),
        ("finished", "FINISHED"),
        ("archived", "ARCHIVED"),
    ]
    title = models.CharField(_("title"), max_length=256)
    course = models.ForeignKey("common.Course", on_delete=models.SET_NULL, verbose_name="course", related_name="groups", null=True)
    teacher = models.ForeignKey("common.Teacher", on_delete=models.SET_NULL, verbose_name="teacher", related_name="groups", null=True)
    lesson_days = models.CharField(_("lesson days"), max_length=256, choices=day_choices)
    time = models.TimeField(_("time"))
    date_started = models.DateField()
    status = models.CharField(_("status"), max_length=256, choices=status_choices, default="ACTIVE") 

    class Meta:
        db_table = "groups"
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.title


class Student(BaseModel):
    status_choices = [

    ]
    full_name = models.CharField(_("full name"), max_length=256)
    group = models.ForeignKey("common.Group", on_delete=models.CASCADE, verbose_name="group", related_name="students")
    birth_date = models.DateField(_("birth date"))
    phone = models.CharField(_("phone"), max_length=256)
    address = models.CharField(_("address"), max_length=256)
    balance = models.IntegerField(_("balance"))
    date_joined = models.DateTimeField(_("date joined"))
    status = models.CharField(_("status"), max_length=256, choices=status_choices)

    class Meta:
        db_table = "students"
        verbose_name = _("student")
        verbose_name_plural = _("students")

    def __str__(self):
        return self.phone


class Attendance(BaseModel):
    student_group = models.ForeignKey("common.Group", on_delete=models.SET_NULL, verbose_name="student group", related_name="attendances", null=True)
    student = models.ForeignKey("common.Student", on_delete=models.SET_NULL, verbose_name="student", related_name="student", null=True)
    is_present = models.BooleanField(_("is present"))
    grade = models.PositiveIntegerField(_("grade"), validators=[MinValueValidator(1), MaxValueValidator(10)])
    date_time = models.DateTimeField(_("date time"))

    class Meta:
        db_table = "attendances"
        verbose_name = _("attendance")
        verbose_name_plural = _("students")

    def __str__(self):
        return self.student.phone


class Lead(BaseModel):
    status_choices = [
    ]
    full_name = models.CharField(_("full name"), max_length=256)
    birth_date = models.DateField(_("birth date"))
    phone = models.CharField(_("phone"), max_length=256)
    address = models.CharField(_("address"), max_length=256)
    interested_course = models.ForeignKey("common.Course", on_delete=models.SET_NULL, verbose_name="interested course", related_name="leads", null=True) 
    status = models.CharField(_("status"), max_length=256, choices=status_choices)

    class Meta:
        db_table = "leads"
        verbose_name = _("lead")
        verbose_name_plural = _("leads")

    def __str__(self):
        return self.phone



