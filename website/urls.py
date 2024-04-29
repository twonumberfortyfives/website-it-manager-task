from django.urls import path
from website.views import (
    my_page_url,
    WorkerListView,
    WorkerDetailView,
    WorkerUpdateView,
    WorkerCreateView,
    WorkerDeleteView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDetailView,
    PositionDeleteView,
    TaskDetailView,
    TaskListView,
    TaskCreateView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeDeleteView,
)

urlpatterns = [
    path('my-page/', my_page_url, name="my-page"),
    path("tasks/", TaskListView.as_view(), name='tasks-list'),
    path("tasks/create", TaskCreateView.as_view(), name='tasks-create'),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="tasks-detail"),
    path("task-types/", TaskTypeListView.as_view(), name='task-type-list'),
    path("task-types/create/", TaskTypeCreateView.as_view(), name='task-type-create'),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name='task-type-delete'),
    path("workers/", WorkerListView.as_view(), name="workers-list"),
    path("workers/create", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete", WorkerDeleteView.as_view(), name="worker-delete"),
    path("positions/", PositionListView.as_view(), name="positions-list"),
    path("positions/create", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/detail", PositionDetailView.as_view(), name="position-detail"),
    path("positions/<int:pk>/delete", PositionDeleteView.as_view(), name="position-delete"),
]

app_name = "website"
