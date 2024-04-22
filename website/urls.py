from django.urls import path
from website.views import index, WorkerListView

urlpatterns = [
    path("index/", index, name="index"),
    path("workers", WorkerListView.as_view(), name="workers-list")
]

app_name = "website"
