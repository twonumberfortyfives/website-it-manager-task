from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from website import forms
from website.forms import WorkerSearchForm
from website.models import Worker, Position


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'website/index.html')


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "website/workers_list.html"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get('username', '')
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


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


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    template_name = "website/worker_form.html"
    success_url = reverse_lazy("website:workers-list")
    form_class = forms.WorkerForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "website/worker_delete_confirm.html"
    success_url = reverse_lazy("website:workers-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    form_class = forms.PositionSearchForm
    context_object_name = "position_list"
    template_name = "website/positions_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = forms.PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = forms.PositionSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    success_url = reverse_lazy("website:positions-list")
    form_class = forms.PositionForm
    template_name = "website/positions_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = forms.PositionForm
    template_name = "website/positions_form.html"

    def get_success_url(self):
        return reverse_lazy("website:", kwargs={"pk": self.object.id})


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    form_class = forms.PositionForm
    template_name = "website/positions_detail.html"
    context_object_name = "position_detail"
