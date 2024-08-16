from django.contrib.auth.models import User
from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class File(models.Model):
    file = models.FileField(upload_to='files')
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SharedFile(models.Model):
    READ_ONLY = 'read_only'
    EDIT = 'edit'

    PERMISSION_CHOICES = [
        (READ_ONLY, 'Read only'),
        (EDIT, 'Edit'),
        ]

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.IntegerField(choices=PERMISSION_CHOICES)

    def __str__(self):
        return f"{self.file.name} shared with {self.shared_with.username}"
