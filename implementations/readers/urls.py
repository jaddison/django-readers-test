from django.urls import path

from .views import AuthorListView

urlpatterns = [
    path('authors/', AuthorListView.as_view(), name="readers-authors"),
]
