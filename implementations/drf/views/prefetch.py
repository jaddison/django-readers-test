from data.models import Author
from .basic import BasicAuthorListView


class PrefetchAuthorListView(BasicAuthorListView):
    queryset = Author.objects.all().prefetch_related("book_set")
