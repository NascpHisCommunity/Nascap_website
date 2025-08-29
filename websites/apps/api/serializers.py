# apps/api/serializers.py
from rest_framework import serializers
from apps.file_manager.models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'title', 'description', 'file', 'uploaded_at')
