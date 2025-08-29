import django_filters
from .models import File

class FileFilter(django_filters.FilterSet):
    """
    Provides filtering for the File model, allowing searches by title, category,
    file type, and a range of creation dates.
    """
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title contains'
    )
    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='icontains',
        label='Category contains'
    )
    file_type = django_filters.ChoiceFilter(
        field_name='file_type',
        choices=File.FILE_TYPE_CHOICES,
        label='File Type'
    )
    created_at = django_filters.DateFromToRangeFilter(
        field_name='created_at',
        label='Created Date Range'
    )

    class Meta:
        model = File
        # The fields list defines which model fields are filterable.
        fields = ['title', 'category', 'file_type', 'created_at']
