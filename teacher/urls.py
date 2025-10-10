from django.urls import path
from teacher import views
app_name = "teacher"

urlpatterns = [
    path("", views.HomeView.as_view(), name='home')
]
