# apps/api/views.py
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.content_creator.models import Content
from apps.file_manager.models import File


def get_ordered_values(model, filter_kwargs, ordering, limit=None, values=None):
    """
    Return a list of dicts for model instances filtered by filter_kwargs,
    ordered by 'ordering'. If limit is provided, slice the queryset.
    Optional 'values' lets you control fields returned explicitly.
    """
    qs = model.objects.filter(**filter_kwargs).order_by(*ordering)
    if limit is not None:
        qs = qs[:limit]
    if values:
        qs = qs.values(*values)
    else:
        qs = qs.values()
    return list(qs)


# -------------------------
# File serialization helper
# -------------------------

def serialize_files(qs):
    """
    Turn File queryset into the exact shape your frontend expects:
    - title
    - file_type
    - url            (computed from FileField .url)
    - thumbnail_url  (computed if you have a thumbnail ImageField)
    - category
    - created_at / updated_at (ISO serialized by DRF)
    """
    out = []
    for f in qs:
        out.append({
            "id": f.id,
            "title": getattr(f, "title", "") or "",
            "file_type": getattr(f, "file_type", "") or "",
            "url": (f.file.url if getattr(f, "file", None) else ""),
            "thumbnail_url": (
                f.thumbnail.url if getattr(f, "thumbnail", None) else ""
            ),
            "category": getattr(f, "category", "") or "",
            "created_at": f.created_at,
            "updated_at": f.updated_at,
        })
    return out


# -------------------------
# File-related endpoints
# -------------------------

@api_view(['GET'])
def FileListAPIView(request):
    qs = File.objects.all().order_by("-created_at")
    return Response(serialize_files(qs))


@api_view(['GET'])
def top_reports_files(request):
    qs = File.objects.filter(
        category__iexact="reports"
    ).order_by("-updated_at", "-created_at")[:4]
    return Response(serialize_files(qs))


@api_view(['GET'])
def top_publications_files(request):
    qs = File.objects.filter(
        category__iexact="publications"
    ).order_by("-updated_at", "-created_at")[:4]
    return Response(serialize_files(qs))


@api_view(['GET'])
def top_resources_files(request):
    qs = File.objects.filter(
        category__iexact="resources"
    ).order_by("-updated_at", "-created_at")[:4]
    return Response(serialize_files(qs))


@api_view(['GET'])
def top_analysis_files(request):
    qs = File.objects.filter(
        category__iexact="analysis"
    ).order_by("-updated_at", "-created_at")[:4]
    return Response(serialize_files(qs))


@api_view(['GET'])
def all_reports_files_by_slug(request):
    qs = File.objects.filter(
        category__iexact="reports"
    ).order_by("-updated_at", "-created_at")
    return Response(serialize_files(qs))


@api_view(['GET'])
def all_publications_files(request):
    qs = File.objects.filter(
        category__iexact="publications"
    ).order_by("-updated_at", "-created_at")
    return Response(serialize_files(qs))


@api_view(['GET'])
def all_resources_files(request):
    qs = File.objects.filter(
        category__iexact="resources"
    ).order_by("-updated_at", "-created_at")
    return Response(serialize_files(qs))


@api_view(['GET'])
def top_video_files(request):
    qs = File.objects.filter(
        file_type__iexact="video"
    ).order_by("-updated_at", "-created_at")[:3]
    return Response(serialize_files(qs))


@api_view(['GET'])
def top_image_files(request):
    qs = File.objects.filter(
        file_type__iexact="image"
    ).order_by("-updated_at", "-created_at")[:3]
    return Response(serialize_files(qs))


@api_view(['GET'])
def all_video_files(request):
    qs = File.objects.filter(
        file_type__iexact="video"
    ).order_by("-updated_at", "-created_at")
    return Response(serialize_files(qs))


@api_view(['GET'])
def all_image_files(request):
    qs = File.objects.filter(
        file_type__iexact="image"
    ).order_by("-updated_at", "-created_at")
    return Response(serialize_files(qs))


# -------------------------
# Content-related endpoints
# -------------------------

@api_view(['GET'])
def latest_news_events(request):
    """
    Last 30 days of published news/events.
    (Note: content_type uses singular 'event')
    """
    cutoff = timezone.now() - timedelta(days=30)
    qs = Content.objects.filter(
        Q(content_type__in=["news", "event"]),
        published=True
    ).filter(
        Q(published_at__gte=cutoff) | Q(created_at__gte=cutoff)
    ).order_by("-published_at", "-created_at")

    # Keep payload tidy for your carousel:
    data = list(qs.values("id", "title", "body", "created_at"))
    return Response(data)


@api_view(['GET'])
def department_contents(request):
    qs = Content.objects.filter(
        content_type__iexact="department",
        published=True
    ).order_by("-published_at", "-created_at")
    data = list(qs.values("id", "title", "slug"))
    return Response(data)


@api_view(['GET'])
def all_analysis_contents(request):
    """
    Any published content linked to 'analysis' category.
    (No restriction to content_type unless you prefer blog-only.)
    """
    qs = Content.objects.filter(
        category__name__iexact="analysis",
        published=True
    ).order_by("-published_at", "-created_at")
    return Response(list(qs.values()))


@api_view(['GET'])
def top_news_contents(request):
    qs = Content.objects.filter(
        content_type__iexact="news", published=True
    ).order_by("-published_at", "-created_at")[:4]
    return Response(list(qs.values()))


@api_view(['GET'])
def top_events_contents(request):
    qs = Content.objects.filter(
        content_type__iexact="event", published=True
    ).order_by("-published_at", "-created_at")[:4]
    return Response(list(qs.values()))


@api_view(['GET'])
def top_blogs_contents(request):
    qs = Content.objects.filter(
        content_type__iexact="blog", published=True
    ).order_by("-published_at", "-created_at")[:4]
    return Response(list(qs.values()))


@api_view(['GET'])
def top_projects_contents(request):
    """
    Treat 'projects' as a Category (not content_type).
    """
    qs = Content.objects.filter(
        category__name__iexact="projects", published=True
    ).order_by("-published_at", "-created_at")[:4]
    return Response(list(qs.values()))


@api_view(['GET'])
def all_news_contents(request):
    qs = Content.objects.filter(
        content_type__iexact="news", published=True
    ).order_by("-published_at", "-created_at")
    return Response(list(qs.values()))


@api_view(['GET'])
def all_events_contents(request):
    qs = Content.objects.filter(
        content_type__iexact="event", published=True
    ).order_by("-published_at", "-created_at")
    return Response(list(qs.values()))


@api_view(['GET'])
def all_blogs_contents(request):
    qs = Content.objects.filter(
        content_type__iexact="blog", published=True
    ).order_by("-published_at", "-created_at")
    return Response(list(qs.values()))


@api_view(['GET'])
def all_projects_contents(request):
    qs = Content.objects.filter(
        category__name__iexact="projects", published=True
    ).order_by("-published_at", "-created_at")
    return Response(list(qs.values()))


@api_view(['GET'])
def all_analysis_files(request):
    """
    All analysis files (File model) – keep this name so it matches your urls.py.
    """
    qs = File.objects.filter(
        category__iexact="analysis"
    ).order_by("-updated_at", "-created_at")
    return Response(serialize_files(qs))
