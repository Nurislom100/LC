from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('status/', views.status_view, name='status'),
    path('admin-login/', views.admin_login, name='admin-login'),
    path('admin/', views.admin_panel, name='admin-panel'),
    path('admin/approve/<int:receipt_id>/', views.admin_approve_receipt, name='admin-approve'),
    path('admin/reject/<int:receipt_id>/', views.admin_reject_receipt, name='admin-reject'),
]