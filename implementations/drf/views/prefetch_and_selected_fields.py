from django.db.models import Prefetch

from data.models import Author, Book
from .basic import BasicAuthorListView


class PrefetchAndSelectedFieldsAuthorListView(BasicAuthorListView):
    queryset = Author.objects.only(
        "id",
        "first_name",
        "last_name",
        "created",
        "updated",
    ).prefetch_related(Prefetch("book_set", queryset=Book.objects.only(
        "id",
        "created",
        "updated",
        "isbn",
        "title",
        "published",
        "author_id"
    )))
