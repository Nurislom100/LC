from django.shortcuts import render
from django.views.generic import View
from common.mixins import RoleRequiredMixin
from common import models
from django.views.generic import TemplateView, ListView, View
from common import mixins


class TeacherHomeView(mixins.RoleRequiredMixin, TemplateView):
    template_name = "teacher/base/index.html"
    allowed_roles = ['teacher']
