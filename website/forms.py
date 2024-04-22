from django import forms
from django.contrib.auth.forms import UserCreationForm

from website.models import Worker


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
                "placeholder": "Search by name"
            }
        )
    )
