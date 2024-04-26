from django import forms
from django.contrib.auth.forms import UserCreationForm

from website.models import Worker, Position, Task


class WorkerForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("position", "first_name", "last_name", "email", "username")


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )
    )


class PositionForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Position
        fields = "__all__"


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class TaskForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "assignees")
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )
