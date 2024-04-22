from django.urls import path
from website.views import (
    index,
    WorkerListView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerCreateView,
    WorkerDeleteView,
)

urlpatterns = [
    path("index/", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="workers-list"),
    path("workers/create", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete", WorkerDeleteView.as_view(), name="worker-delete"),
]

app_name = "website"
