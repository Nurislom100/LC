from django.shortcuts import render
from django.views.generic import View
from helpers.permissions import AccountantPassesTestMixin
from common import models



class HomeView(AccountantPassesTestMixin, View):
    def get(self, request):
        print(request.user.role)
        return render(request, "accountant/base/index.html")


