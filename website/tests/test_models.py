from django.test import TestCase

from website.models import TaskType, Position, Worker, Task


class TestModels(TestCase):
    def test_task_type_str(self):
        task_type = TaskType(name="test1")
        self.assertEqual(str(task_type), task_type.name)

    def test_position_str(self):
        position = Position(name="test2")
        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        position = Position(name="test3")
        worker = Worker(
            position=position,
            username="username",
            email="email@gmail.com",
            first_name="first",
            last_name="last",
        )
        self.assertEqual(str(worker), worker.username)
