import django_tables2 as tables
from .models import File

class FileTable(tables.Table):
    # The title column is linked to the file's detail page using the model's get_absolute_url() method.
    title = tables.Column(linkify=True)
    
    # A custom preview column that renders different content based on the file type.
    preview = tables.TemplateColumn(
        template_code="""
            {% if record.file_type == 'image' %}
                <img src="{{ record.file.url }}" alt="{{ record.title }}" style="max-height: 50px;" />
            {% elif record.file_type == 'document' %}
                <a href="{{ record.file.url }}" target="_blank">View Document</a>
            {% elif record.file_type == 'video' %}
                <a href="{{ record.file.url }}" target="_blank">Watch Video</a>
            {% else %}
                N/A
            {% endif %}
        """,
        verbose_name="Preview",
        orderable=False
    )
    
    # Other columns displaying file metadata.
    file_type = tables.Column(verbose_name="Type")
    category = tables.Column()
    created_at = tables.DateTimeColumn(format="Y-m-d H:i:s", verbose_name="Uploaded On")
    updated_at = tables.DateTimeColumn(format="Y-m-d H:i:s", verbose_name="Last Updated")
    
    class Meta:
        model = File
        # Specify the order and which fields to include in the table.
        fields = ("title", "preview", "file_type", "category", "created_at", "updated_at")
        # Use a Bootstrap4 template; adjust if you are using a different framework.
        template_name = "django_tables2/bootstrap4.html"
