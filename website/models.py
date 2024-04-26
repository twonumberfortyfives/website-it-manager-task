from django.contrib.auth.models import AbstractUser
from django.db import models

from website_it_manager_task.settings import AUTH_USER_MODEL


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE, related_name="workers")

    class Meta:
        verbose_name_plural = "workers"
        ordering = ["id"]

    def __str__(self):
        return self.username


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('low', 'Low'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(AUTH_USER_MODEL, related_name="tasks_assigned")
