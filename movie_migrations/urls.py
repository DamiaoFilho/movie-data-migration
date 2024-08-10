from django.shortcuts import render
# Create your views here.



from django.urls import path
from .views import MigrationView

urlpatterns = [
    path("", MigrationView.as_view(), name="migration-form")
]