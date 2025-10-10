from django.urls import path
from accountant import views
app_name = "accountant"

urlpatterns = [
         path("", views.HomeView.as_view(), name='home'),
]
