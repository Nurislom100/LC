from django.shortcuts import render
from django.views.generic import View
from helpers.permissions import ReceptionPassesTestMixin

from common import models



class HomeView(ReceptionPassesTestMixin, View):
    def get(self, request):
        print(request.user.role)
        return render(request, "reception/base/index.html")


