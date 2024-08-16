from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ViewSet

from files.models import File, Folder, SharedFile
from files.serialziers import FileSerializer, FolderSerializer, SharedFileSerializer


class FileViewSet(ViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Files",
        operation_description="Retrieve a list of all files owned by the authenticated user.",
        responses={200: FileSerializer(many=True)},
    )
    def list(self, request):
        files = self.queryset.filter(owner=request.user)
        serializer = self.serializer_class(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create File",
        operation_description="Create a new file and associate it with the authenticated user.",
        request_body=FileSerializer,
        responses={201: FileSerializer, 400: 'Bad Request'},
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Retrieve File",
        operation_description="Retrieve a specific file by its ID, if it belongs to the authenticated user.",
        responses={200: FileSerializer, 404: 'Not Found'},
    )
    def retrieve(self, request, pk=None):
        file = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        serializer = self.serializer_class(file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update File",
        operation_description="Update a specific file by its ID, if it belongs to the authenticated user.",
        request_body=FileSerializer,
        responses={200: FileSerializer, 400: 'Bad Request', 404: 'Not Found'},
    )
    def update(self, request, pk=None):
        file = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        serializer = self.serializer_class(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete File",
        operation_description="Delete a specific file by its ID, if it belongs to the authenticated user.",
        responses={204: 'No Content', 404: 'Not Found'},
    )
    def destroy(self, request, pk=None):
        file = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FolderViewSet(ViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Folders",
        operation_description="Retrieve a list of all folders owned by the authenticated user.",
        responses={200: FolderSerializer(many=True)},
    )
    def list(self, request):
        folders = self.queryset.filter(owner=request.user)
        serializer = self.serializer_class(folders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create Folder",
        operation_description="Create a new folder and associate it with the authenticated user.",
        request_body=FolderSerializer,
        responses={201: FolderSerializer, 400: 'Bad Request'},
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Retrieve Folder",
        operation_description="Retrieve a specific folder by its ID, if it belongs to the authenticated user.",
        responses={200: FolderSerializer, 404: 'Not Found'},
    )
    def retrieve(self, request, pk=None):
        folder = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        serializer = self.serializer_class(folder)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update Folder",
        operation_description="Update a specific folder by its ID, if it belongs to the authenticated user.",
        request_body=FolderSerializer,
        responses={200: FolderSerializer, 400: 'Bad Request', 404: 'Not Found'},
    )
    def update(self, request, pk=None):
        folder = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        serializer = self.serializer_class(folder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete Folder",
        operation_description="Delete a specific folder by its ID, if it belongs to the authenticated user.",
        responses={204: 'No Content', 404: 'Not Found'},
    )
    def destroy(self, request, pk=None):
        folder = get_object_or_404(self.queryset, pk=pk, owner=request.user)
        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SharedFileViewSet(ViewSet):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Shared Files",
        operation_description="Retrieve a list of all shared files for the authenticated user.",
        responses={200: SharedFileSerializer(many=True)},
    )
    def list(self, request):
        shared_files = self.queryset.filter(shared_with=request.user)
        serializer = self.serializer_class(shared_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create Shared File",
        operation_description="Create a new shared file with the authenticated user as the recipient.",
        request_body=SharedFileSerializer,
        responses={201: SharedFileSerializer, 400: 'Bad Request'},
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            validated_data = serializer.validated_data
            validated_data['shared_with'] = request.user
            serializer.save(**validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Retrieve Shared File",
        operation_description="Retrieve a specific shared file by its ID, if it belongs to the authenticated user.",
        responses={200: SharedFileSerializer, 404: 'Not Found'},
    )
    def retrieve(self, request, pk=None):
        shared_file = get_object_or_404(self.queryset, pk=pk, shared_with=request.user)
        serializer = self.serializer_class(shared_file)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update Shared File",
        operation_description="Update a specific shared file by its ID, if it belongs to the authenticated user.",
        request_body=SharedFileSerializer,
        responses={200: SharedFileSerializer, 400: 'Bad Request', 404: 'Not Found'},
    )
    def update(self, request, pk=None):
        shared_file = get_object_or_404(self.queryset, pk=pk, shared_with=request.user)
        serializer = self.serializer_class(shared_file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete Shared File",
        operation_description="Delete a specific shared file by its ID, if it belongs to the authenticated user.",
        responses={204: 'No Content', 404: 'Not Found'},
    )
    def destroy(self, request, pk=None):
        shared_file = get_object_or_404(self.queryset, pk=pk, shared_with=request.user)
        shared_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
