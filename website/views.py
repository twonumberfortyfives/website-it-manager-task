from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from website import forms
from website.models import Worker


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'website/index.html')


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "website/workers_list.html"
    paginate_by = 2


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker_detail"
    template_name = "website/worker_detail.html"


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    template_name = "website/worker_form.html"
    form_class = forms.WorkerForm

    def get_success_url(self):
        return reverse_lazy("website:worker-detail", kwargs={'pk': self.object.pk})
