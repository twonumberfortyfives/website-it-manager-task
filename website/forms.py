from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from website.models import Worker, Position, Task, TaskType


class WorkerForm(forms.ModelForm):
    position = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select,
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("position", "first_name", "last_name", "email", "username")

    def clean_position(self):
        position = self.cleaned_data.get('position')
        if not position:
            raise forms.ValidationError("Please select a position.")
        return position


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
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

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


class TaskTypeSearchForm(forms.Form):
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


class TaskTypeForm(forms.Form):
    class Meta(forms.Form):
        model = TaskType
        fields = "__all__"
