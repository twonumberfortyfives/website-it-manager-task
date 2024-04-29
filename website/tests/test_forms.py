from django.test import TestCase
from website.forms import WorkerForm
from website.models import Position


class FormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )

    def test_create_user_form_with_position(self):
        form_data = {
            "username": "username",
            "email": "email@gmail.com",
            "position": self.position,
            "first_name": "firstname",
            "last_name": "lastname",
        }
        form = WorkerForm(
            data=form_data
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
