# Description: URL patterns for the frontend app
from django.urls import path
from .views import index

urlpatterns = [
    path('', index),  # Home page
]
