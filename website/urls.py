from django.urls import path

from website.views import index

urlpatterns = [
    path("index/", index, name="index"),
]

app_name = "website"
