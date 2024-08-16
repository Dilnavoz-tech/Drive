from django.urls import path
from .views import FileViewSet, FolderViewSet, SharedFileViewSet

urlpatterns = [
    # FileViewSet URLs
    path('files/', FileViewSet.as_view({'get': 'list', 'post': 'create'}), name='file-list-create'),
    path('files/<int:pk>/', FileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='file-detail'),

    # FolderViewSet URLs
    path('folders/', FolderViewSet.as_view({'get': 'list', 'post': 'create'}), name='folder-list-create'),
    path('folders/<int:pk>/', FolderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='folder-detail'),

    # SharedFileViewSet URLs
    path('shared-files/', SharedFileViewSet.as_view({'get': 'list', 'post': 'create'}), name='sharedfile-list-create'),
    path('shared-files/<int:pk>/', SharedFileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='sharedfile-detail'),
]
