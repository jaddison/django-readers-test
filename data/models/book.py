import uuid

from django.db import models


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    isbn = models.CharField(max_length=20, blank=True, default="", db_index=True)
    title = models.CharField(max_length=100, blank=True, default="")
    subtitle = models.CharField(max_length=512, blank=True, default="")
    snippet = models.TextField(blank=True, default="")
    published = models.DateField(blank=True, null=True)

    author = models.ForeignKey("data.Author", on_delete=models.CASCADE)

