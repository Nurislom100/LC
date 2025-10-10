from django.urls import path
from reception import views
app_name = "reception"

urlpatterns = [
        path("", views.HomeView.as_view(), name='home')

]
