from django.contrib import admin
from django.urls import path, include  # include lets you add app urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),  # this links the polls app urls
]
