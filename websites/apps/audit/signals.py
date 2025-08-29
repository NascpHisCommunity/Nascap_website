from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import AuditLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditLog.objects.create(
        user=user,
        action='login',
        ip_address=ip,
        path=request.path,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditLog.objects.create(
        user=user,
        action='logout',
        ip_address=ip,
        path=request.path,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditLog.objects.create(
        user=None,
        action='failed_login',
        ip_address=ip,
        path=request.path,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        additional_data={'credentials': credentials},
    )
