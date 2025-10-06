from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from common import models
from manager import forms
from helpers.permissions import ManagerPassesTestMixin
from helpers.views import CreateView, UpdateView, DeleteView

class HomeView(ManagerPassesTestMixin, View):
    def get(self, request):
        print(request.user.role)
        return render(request, "base/index.html")

class BaseUserListView(ListView):
    model = models.BaseUser
    template_name = "forms/user/list.html"
    context_object_name = "objects"
    queryset = models.BaseUser.objects.all().order_by("-id")
    paginate_by = 10


class BaseUserCreateView(CreateView):
    model = models.BaseUser
    form_class = forms.BaseUserForm
    template_name = "forms/user/create.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_create_url = "manager:user-create"


class BaseUserUpdateView(UpdateView):
    model = models.BaseUser
    form_class = forms.BaseUserForm
    template_name = "forms/user/update.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_create_url = "manager:user-update"
