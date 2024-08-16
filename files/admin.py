from django.contrib import admin

from files.models import File, Folder, SharedFile

admin.site.register(File)
admin.site.register(Folder)
admin.site.register(SharedFile)
