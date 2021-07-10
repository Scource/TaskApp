from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import reverse
from ..models import *
from django.contrib.auth.models import AnonymousUser, User


class IndexViewTest(TestCase):

    def test_index_route(self):
        client = APIClient()
        response = client.get(reverse('resizer:index-list'))
        self.assertEqual(response.status_code, 200)


class FileUploadViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        upload_file_data = {'title': 'new idea',
                            'user': 1,
                            }

    def test_upload_correct_file(self):
        factory = APIRequestFactory()
        factory.post(reverse('resizer:upload-list'), {'title': 'new idea'})
