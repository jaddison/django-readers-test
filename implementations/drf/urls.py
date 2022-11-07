from django.urls import path

from .views.basic import BasicAuthorListView
from .views.prefetch import PrefetchAuthorListView
from .views.prefetch_and_selected_fields import PrefetchAndSelectedFieldsAuthorListView

urlpatterns = [
    path('authors/basic/', BasicAuthorListView.as_view()),
    path('authors/with-prefetch/', PrefetchAuthorListView.as_view()),
    path('authors/with-prefetch-and-selected-fields/', PrefetchAndSelectedFieldsAuthorListView.as_view()),
]
