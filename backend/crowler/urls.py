from django.urls import path

from . import views

urlpatterns = [
    path("url/", views.get_url, name="get_url"),  # Render the form to collect the URL
    path("crawl/", views.index, name="index"),  # Trigger the spider with the provided URL
]
"""
urlpatterns = [
    path("", views.index, name="index"),
    path('', views.get_url, name='get_url'),
]
"""