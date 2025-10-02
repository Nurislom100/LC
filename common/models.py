from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


from helpers.models import BaseModel


class User(AbstractUser):
    role_choices = [
        ("manager", "Manager"),
        ("reception", "Reception"),
        ("accountant", "Accountant"),
        ("teacher", "Teacher"),
    ]
    full_name = models.CharField(_("full name"), max_length=256, null=True, blank=True)
    username = models.CharField(_("username"), max_length=256, unique=True)
    phone = models.CharField(_("phone"), max_length=256)
    role = models.CharField(_("role"), max_length=256, choices=role_choices)
    teacher_profile = models.ForeignKey("common.Teacher", on_delete=models.CASCADE, verbose_name="teacher profile", related_name="user")
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
    price = models.DecimalField()

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
    course = models.ForeignKey("common.Course", on_delete=models.SET_NULL, verbose_name="course", related_name="groups")
    teacher = models.ForeignKey("common.Teacher", on_delete=models.SET_NULL, verbose_name="teacher", related_name="groups")
    lesson_days = models.CharField(_("lesson days"), max_length=256, choices=day_choices)
    time = models.TimeField(_("time"))
    date_started = models.DateField(auto_now_add=True)
    status = models.CharField(_("status"), max_length=256, choices=status_choices, default="ACTIVE") 

    class Meta:
        db_table = "groups"
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.title



