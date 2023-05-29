from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class MusicFile(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'

    UPLOAD_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PROTECTED, 'Protected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music_files/')
    upload_type = models.CharField(
        max_length=10, choices=UPLOAD_CHOICES, default=PUBLIC)
    allowed_emails = models.TextField(blank=True)

    def __str__(self):
        return self.title
