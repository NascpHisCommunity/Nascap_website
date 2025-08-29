from django.views.generic import TemplateView
from django.db.models import Count
from .models import AuditLog

class AuditDashboardView(TemplateView):
    template_name = 'audit/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggregate page views grouped by path
        page_views = AuditLog.objects.filter(action='page_view') \
            .values('path') \
            .annotate(count=Count('id')) \
            .order_by('-count')
        # Count unique visitor IPs for page views
        total_visitors = AuditLog.objects.filter(action='page_view') \
            .values('ip_address') \
            .distinct() \
            .count()
        context['page_views'] = page_views
        context['total_visitors'] = total_visitors
        return context
