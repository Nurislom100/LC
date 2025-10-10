from django.shortcuts import render
from django.views.generic import View
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from common import models
from helpers.views import CreateView, UpdateView, DeleteView


class HomeView(View):
    def get(self, request):
        return render(request, "base/index.html")

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return self.redirect_by_role(request.user)
        return render(request, "base/user/login.html")

    def post(self, request):
        req = request.POST.dict()
        username = req.get("username")
        password = req.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return self.redirect_by_role(user)
        else:
            return render(request, "base/user/login.html", {"error": True})

    def redirect_by_role(self, user):
        if user.role == "manager":
            return HttpResponseRedirect(reverse_lazy("manager:home"))
        if user.role == "accountant":
            return HttpResponseRedirect(reverse_lazy("accountant:home"))
        if user.role == "reception":
            return HttpResponseRedirect(reverse_lazy("reception:home"))
        if user.role == "teacher":
            return HttpResponseRedirect(reverse_lazy("teacher:home"))
        raise PermissionDenied("You don't have access to this page")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy("login"))


