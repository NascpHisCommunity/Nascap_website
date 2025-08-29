from django.urls import path
from .views import AuditDashboardView

app_name = 'audit'

urlpatterns = [
    path('dashboard/', AuditDashboardView.as_view(), name='dashboard'),
]
