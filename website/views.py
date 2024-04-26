from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from website import forms
from website.forms import WorkerSearchForm, TaskForm, TaskSearchForm
from website.models import Worker, Position, Task, TaskType


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    context_object_name = 'task_detail'
    template_name = 'website/index.html'
    success_url = reverse_lazy('website:tasks-list')


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = 'website/task_list.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get('name', '')
        context['total_tasks_count'] = Task.objects.all().count()
        context['search_form'] = TaskSearchForm(
            initial={'name': name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all().prefetch_related("assignees").select_related("task_type")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data['name'])
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('website:tasks-list')


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
        context["total_workers_count"] = self.get_queryset().count()
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position").all()
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
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["total_positions_count"] = self.get_queryset().count()
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
        return reverse_lazy("website:position-detail", kwargs={"pk": self.object.id})


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    form_class = forms.PositionForm
    template_name = "website/positions_detail.html"
    context_object_name = "position_detail"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("website:positions-list")
    template_name = "website/positions_delete_confirm.html"


def my_page_url(request: HttpRequest) -> HttpResponse:
    my_positions = Position.objects.filter(workers=request.user)
    my_tasks = Task.objects.filter(assignees=request.user)
    context = {
        "my_positions": my_positions,
        "my_tasks": my_tasks,
    }
    return render(request, template_name="website/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    form_class = forms.TaskTypeSearchForm
    context_object_name = "task_type_list"
    template_name = "website/task_type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = forms.TaskTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = forms.TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset
