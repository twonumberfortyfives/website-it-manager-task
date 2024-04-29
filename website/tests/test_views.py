from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client

from website.models import Worker, Position

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
        position = Position.objects.create(
            name="Test Position"
        )

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
        self.assertTemplateUsed(response, "website/workers_list.html")


class PublicPositionTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(POSITION_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        position = Position.objects.create(
            name="Test Position"
        )

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
        self.assertTemplateUsed(response, "website/positions_list.html")
        self.assertQuerysetEqual(response.context["position_list"], all_positions)
