from django.shortcuts import render
from django.views.generic import View
from django.views.generic import ListView

from common import models
from helpers.views import CreateView, UpdateView, DeleteView


class HomeView(View):
    def get(self, request):
        return render(request, "base/index.html")


