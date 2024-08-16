from rest_framework import serializers
from .models import File, Folder, SharedFile

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'name', 'folder', 'owner', 'created_at']

class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'owner', 'created_at', 'files']

class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ['id', 'file', 'shared_with', 'permission']
