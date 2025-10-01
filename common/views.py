from django.shortcuts import render
from django.views.generic import View
from common import models

class HomeView(View):
    def get(self, request):
        return render(request, "base/index.html")
