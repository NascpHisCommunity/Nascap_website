from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.content_creator.models import Content
from apps.file_manager.models import File

def get_ordered_values(model, filter_kwargs, ordering, limit=None):
    """
    Return a list of dictionaries for the model instances filtered by filter_kwargs,
    ordered by the given ordering. If limit is provided, slice the queryset.
    """
    qs = model.objects.filter(**filter_kwargs).order_by(*ordering)
    if limit is not None:
        qs = qs[:limit]
    return list(qs.values())

# -------------------------
# File-related endpoints
# -------------------------

@api_view(['GET'])
def FileListAPIView(request):
    # List all File items ordered by created_at descending.
    data = get_ordered_values(File, {}, ["-created_at"])
    return Response(data)

@api_view(['GET'])
def top_reports_files(request):
    data = get_ordered_values(File, {"category__iexact": "reports"}, ["-updated_at", "-created_at"], limit=4)
    return Response(data)

@api_view(['GET'])
def top_publications_files(request):
    data = get_ordered_values(File, {"category__iexact": "publications"}, ["-updated_at", "-created_at"], limit=4)
    return Response(data)

@api_view(['GET'])
def top_resources_files(request):
    data = get_ordered_values(File, {"category__iexact": "resources"}, ["-updated_at", "-created_at"], limit=4)
    return Response(data)

@api_view(['GET'])
def top_analysis_files(request):
    data = get_ordered_values(File, {"category__iexact": "analysis"}, ["-updated_at", "-created_at"], limit=4)
    return Response(data)

@api_view(['GET'])
def all_reports_files_by_slug(request):
    data = get_ordered_values(File, {"category__iexact": "reports"}, ["-updated_at", "-created_at"])
    return Response(data)

@api_view(['GET'])
def all_publications_files(request):
    data = get_ordered_values(File, {"category__iexact": "publications"}, ["-updated_at", "-created_at"])
    return Response(data)

@api_view(['GET'])
def all_resources_files(request):
    data = get_ordered_values(File, {"category__iexact": "resources"}, ["-updated_at", "-created_at"])
    return Response(data)

@api_view(['GET'])
def top_video_files(request):
    data = get_ordered_values(File, {"file_type__iexact": "video"}, ["-updated_at", "-created_at"], limit=3)
    return Response(data)

@api_view(['GET'])
def top_image_files(request):
    data = get_ordered_values(File, {"file_type__iexact": "image"}, ["-updated_at", "-created_at"], limit=3)
    return Response(data)

@api_view(['GET'])
def all_video_files(request):
    data = get_ordered_values(File, {"file_type__iexact": "video"}, ["-updated_at", "-created_at"])
    return Response(data)

@api_view(['GET'])
def all_image_files(request):
    data = get_ordered_values(File, {"file_type__iexact": "image"}, ["-updated_at", "-created_at"])
    return Response(data)

# -------------------------
# Content-related endpoints
# -------------------------

@api_view(['GET'])
def latest_news_events(request):
    cutoff = timezone.now() - timedelta(days=30)
    # Use a compound Q filter for news OR events with created_at >= cutoff.
    qs = Content.objects.filter(
        Q(content_type__iexact="news") | Q(content_type__iexact="events"),
        created_at__gte=cutoff
    ).order_by("-created_at")
    return Response(list(qs.values()))

@api_view(['GET'])
def department_contents(request):
    data = get_ordered_values(Content, {"content_type__iexact": "department"}, ["-created_at"])
    return Response(data)

# For Content endpoints, filtering by category is done via a related field (assuming a relation exists)
@api_view(['GET'])
def all_analysis_files(request):
    data = get_ordered_values(Content, {"category__name__iexact": "analysis"}, ["-updated_at", "-created_at"])
    return Response(data)

@api_view(['GET'])
def top_news_contents(request):
    data = get_ordered_values(Content, {"category__name__iexact": "news"}, ["-updated_at", "-created_at"], limit=4)
    return Response(data)

@api_view(['GET'])
def top_events_contents(request):
    data = get_ordered_values(Content, {"category__name__iexact": "events"}, ["-updated_at", "-created_at"], limit=4)
    return Response(data)

@api_view(['GET'])
def top_blogs_contents(request):
    data = get_ordered_values(Content, {"category__name__iexact": "blogs"}, ["-updated_at", "-created_at"], limit=4)
    return Response(data)

@api_view(['GET'])
def top_projects_contents(request):
    data = get_ordered_values(Content, {"category__name__iexact": "projects"}, ["-updated_at", "-created_at"], limit=4)
    return Response(data)

@api_view(['GET'])
def all_news_contents(request):
    data = get_ordered_values(Content, {"category__name__iexact": "news"}, ["-updated_at", "-created_at"])
    return Response(data)

@api_view(['GET'])
def all_events_contents(request):
    data = get_ordered_values(Content, {"category__name__iexact": "events"}, ["-updated_at", "-created_at"])
    return Response(data)

@api_view(['GET'])
def all_blogs_contents(request):
    data = get_ordered_values(Content, {"category__name__iexact": "blogs"}, ["-updated_at", "-created_at"])
    return Response(data)

@api_view(['GET'])
def all_projects_contents(request):
    data = get_ordered_values(Content, {"category__name__iexact": "projects"}, ["-updated_at", "-created_at"])
    return Response(data)
