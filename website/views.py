from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from website.models import Worker


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'website/index.html')


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "website/workers_list.html"
    paginate_by = 2