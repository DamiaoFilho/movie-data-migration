from django.shortcuts import render
# Create your views here.



from django.urls import path
from .views import MigrationView, InfoFile, MovieListView

urlpatterns = [
    path("", MigrationView.as_view(), name="migration-form"),
    path("file", InfoFile.as_view(), name="file-info"),
    path("titles", MovieListView.as_view(), name="titles-list"),
]