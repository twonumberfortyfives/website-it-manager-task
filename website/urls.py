from django.urls import path
from website.views import (
    index,
    WorkerListView,
    WorkerDetailView,
    WorkerUpdateView,
)

urlpatterns = [
    path("index/", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="workers-list"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update", WorkerUpdateView.as_view(), name="worker-update"),
]

app_name = "website"
