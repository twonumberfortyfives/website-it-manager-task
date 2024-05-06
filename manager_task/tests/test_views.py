from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from manager_task.models import Worker, Position, Task, TaskType

TASK_URL = reverse("website:tasks-list")
WORKER_URL = reverse("website:workers-list")
TASK_TYPE_URL = reverse("website:task-type-list")
POSITION_URL = reverse("website:positions-list")


class PublicWorkerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(TASK_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.client = Client()
        position = Position.objects.create(name="Test Position")

        user = Worker.objects.create_user(
            username="username",
            email="email@gmail.com",
            position=position,
            last_name="last_name",
            first_name="first_name",
        )
        self.client.force_login(user)

    def test_get_page_gives_all_workers_and_template_usage(self):
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)
        all_workers = Worker.objects.all()
        self.assertEqual(response.context["total_workers_count"], all_workers.count())
        self.assertQuerysetEqual(response.context["worker_list"], all_workers)
        self.assertTemplateUsed(response, "manager_task/workers_list.html")


class PublicPositionTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(POSITION_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        position = Position.objects.create(name="Test Position")

        user = Worker.objects.create_user(
            username="username",
            email="email@gmail.com",
            position=position,
            last_name="last_name",
            first_name="first_name",
        )
        self.client.force_login(user)

    def test_get_all_positions_and_template_usage(self):
        response = self.client.get(POSITION_URL)
        all_positions = Position.objects.all().order_by("id")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager_task/positions_list.html")
        self.assertQuerysetEqual(response.context["position_list"], all_positions)


class PublicTaskTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(TASK_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.client = Client()
        deadline_date = "2024-05-10"
        task_type = TaskType.objects.create(name="Test Task")
        position = Position.objects.create(name="Test Position")

        user = Worker.objects.create_user(
            username="username",
            email="email@gmail.com",
            position=position,
            last_name="last_name",
            first_name="first_name",
        )

        task = Task.objects.create(
            name="Test name",
            description="description",
            deadline=deadline_date,
            is_completed=False,
            priority="Urgent",
            task_type=task_type,
        )
        task.assignees.add(user)
        task.save()
        self.client.force_login(user)

    def test_get_all_tasks_and_template_usage(self):
        response = self.client.get(TASK_URL)
        all_tasks = Task.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["task_list"], all_tasks)
        self.assertTemplateUsed(response, "manager_task/task_list.html")


class PublicTaskTypeTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        position = Position.objects.create(name="Test Position")
        user = Worker.objects.create_user(
            username="username",
            email="email@gmail.com",
            position=position,
            last_name="last_name",
            first_name="first_name",
        )
        self.client.force_login(user)

    def test_get_all_type_tasks_and_template_usage(self):
        response = self.client.get(TASK_TYPE_URL)
        all_task_types = TaskType.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["task_type_list"], all_task_types)
        self.assertTemplateUsed(response, "manager_task/task_type_list.html")
