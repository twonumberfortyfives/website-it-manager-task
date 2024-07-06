from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
import requests
from ipware import get_client_ip


from manager_task import forms
from manager_task.forms import (
    WorkerSearchForm,
    TaskForm,
    TaskSearchForm,
    CreateMyTaskForm,
    WorkerForm,
    RegistrationForm,
)
from manager_task.models import Worker, Position, Task, TaskType


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    context_object_name = "task_detail"
    template_name = "website/index.html"
    success_url = reverse_lazy("manager_task:tasks-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "website/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["total_tasks_count"] = Task.objects.all().count()
        context["search_form"] = TaskSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = (
            Task.objects.all().prefetch_related("assignees").select_related("task_type")
        )
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager_task:tasks-list")
    template_name = "website/task_form.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager_task:tasks-list")
    template_name = "website/task_form.html"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager_task:tasks-list")
    template_name = "website/task_list_delete_confirm.html"


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "website/workers_list.html"
    paginate_by = 6
    context_object_name = "worker_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(initial={"username": username})
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
        return reverse_lazy("manager_task:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "website/worker_delete_confirm.html"
    success_url = reverse_lazy("manager_task:workers-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    form_class = forms.PositionSearchForm
    context_object_name = "position_list"
    template_name = "website/positions_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["total_positions_count"] = self.get_queryset().count()
        context["search_form"] = forms.PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = forms.PositionSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    success_url = reverse_lazy("manager_task:positions-list")
    form_class = forms.PositionForm
    template_name = "website/positions_form.html"


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = forms.PositionForm
    template_name = "website/positions_form.html"

    def get_success_url(self):
        return reverse_lazy("manager_task:position-detail", kwargs={"pk": self.object.id})


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    form_class = forms.PositionForm
    template_name = "website/positions_detail.html"
    context_object_name = "position_detail"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("manager_task:positions-list")
    template_name = "website/positions_delete_confirm.html"


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    form_class = forms.TaskTypeSearchForm
    context_object_name = "task_type_list"
    template_name = "website/task_type_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["all_task_types"] = TaskType.objects.all().count()
        context["search_form"] = forms.TaskTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = forms.TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = forms.TaskTypeForm
    success_url = reverse_lazy("manager_task:task-type-list")
    template_name = "website/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager_task:task-type-list")
    template_name = "website/task_type_delete_confirm.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = forms.TaskTypeForm
    success_url = reverse_lazy("manager_task:task-type-list")
    template_name = "website/task_type_form.html"


class SearchMyTasksView(LoginRequiredMixin, generic.ListView):
    model = Task
    form_class = forms.MyTaskSearchForm
    template_name = "website/index.html"
    context_object_name = "all_my_tasks"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(
                assignees=self.request.user, name__icontains=name
            )
        else:
            queryset = queryset.filter(assignees=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["total_my_tasks"] = Task.objects.filter(
            assignees=self.request.user
        ).count()
        context["search_form"] = forms.MyTaskSearchForm(initial={"name": name})
        return context


@login_required
def worker_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = WorkerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to database yet
            password = form.cleaned_data["password"]  # Get password from form
            user.set_password(password)  # Hash the password
            user.save()  # Save user to database
            return redirect("website:workers-list")
    else:
        form = WorkerForm()
    return render(request, "website/worker_form.html", {"form": form})


def get_my_profile(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "website/my_profile.html")


@login_required
def create_task_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreateMyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            task.assignees.add(
                request.user
            )  # Add the current user to the assignees ManyToManyField
            form.save_m2m()  # Save the ManyToManyField data
            return redirect("website:my-page")
    else:
        form = CreateMyTaskForm(initial={"assignees": [request.user.id]})
    return render(request, "website/create_my_task.html", context={"form": form})


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "registration/registration.html", {"form": form})


def get_location_from_ip(ip_address):
    url = f"https://freeipapi.com/api/json/{ip_address}"
    response = requests.get(url)
    data = response.json()
    latitude = data['latitude']
    longitude = data['longitude']
    return latitude, longitude


def get_latitude_longitude(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        client_ip, r = get_client_ip(request)
        latitude, longitude = get_location_from_ip(client_ip)
        print(client_ip)
        print(latitude, longitude)
        # Here you can save latitude and longitude to your model or perform any other backend operation
        return HttpResponse({'latitude': latitude, 'longitude': longitude})
