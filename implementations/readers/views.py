from django_readers.rest_framework import SpecMixin
from rest_framework.generics import ListAPIView

from data.models import Author


class AuthorListView(SpecMixin, ListAPIView):
    queryset = Author.objects.all()
    spec = [
        "id",
        "first_name",
        "last_name",
        "created",
        "updated",
        {
            "book_set": [
                "id",
                "created",
                "updated",
                "isbn",
                "title",
                "published",
            ]
        },
    ]
