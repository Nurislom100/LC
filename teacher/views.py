from django.shortcuts import render
from django.views.generic import View
from helpers.permissions import TeacherPassesTestMixin
from common import models

class HomeView(TeacherPassesTestMixin, View):
    def get(self, request):
        print(request.user.role)
        return render(request, "teacher/base/index.html")


