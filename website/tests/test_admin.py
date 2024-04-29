from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from website.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            password='<PASSWORD>123'
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(
            name='Test Position'
        )
        self.worker = get_user_model().objects.create_user(
            username='user',
            password='<PASSWORD>123',
            position=self.position,
        )

    def test_user_position_listed(self):
        url = reverse('admin:website_position_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_user_detail_listed(self):
        url = reverse('admin:website_position_change', args=[self.position.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)
