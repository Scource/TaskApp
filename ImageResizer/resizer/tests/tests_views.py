from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from django.urls import reverse
from ..models import *
from django.contrib.auth.models import User
from ..views import *
from PIL import Image
import tempfile


class IndexViewTest(TestCase):

    def test_index_route(self):
        client = APIClient()
        response = client.get(reverse('resizer:index-list'))
        self.assertEqual(response.status_code, 200)


class ListViewTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.tumbnail = ThumbnailSize.objects.create(
            descriptive_name='test', thumbnail_width=100, thumbnail_height=100)
        self.plan = Plan.objects.create()
        self.plan.size.add(self.tumbnail)
        self.userdetail = UserDetail.objects.create(
            user=self.user, plan=self.plan)

    def test_authorized_user_list_route(self):
        request = self.factory.get(reverse('resizer:list-list'))
        force_authenticate(request, user=self.user)
        response = FileListView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_list_route(self):
        request = self.factory.get(reverse('resizer:list-list'))
        response = FileListView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 403)


class FileUploadViewTest(TestCase):

    def setUp(self):
        # self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.tumbnail = ThumbnailSize.objects.create(
            descriptive_name='test', thumbnail_width=100, thumbnail_height=100)
        self.plan = Plan.objects.create()
        self.plan.size.add(self.tumbnail)
        self.userdetail = UserDetail.objects.create(
            user=self.user, plan=self.plan)

    def test_authorized_user_upload_route(self):
        request = self.factory.get(reverse('resizer:upload-list'))
        force_authenticate(request, user=self.user)
        response = FileUploadView.as_view(
            {'get': 'list', 'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_upload_route(self):
        request = self.factory.get(reverse('resizer:upload-list'))
        response = FileUploadView.as_view(
            {'get': 'list', 'post': 'create'})(request)
        self.assertEqual(response.status_code, 403)

    def test_file_is_accepted(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        request = self.factory.post(
            reverse('resizer:upload-list'), {'file_uploaded': tmp_file, 'user': self.user}, format='multipart')
        # Send data
        with open(tmp_file.name, 'rb') as data:
            force_authenticate(request, user=self.user)
            response = FileUploadView.as_view(
                {'get': 'list', 'post': 'create'})(request)
            self.assertEqual(response.status_code, 200)


class CreateExpiringLinkViewTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.user_with_access = User.objects.create_user(
            username='test2', email='test2@test.com', password='test')
        self.tumbnail = ThumbnailSize.objects.create(
            descriptive_name='test', thumbnail_width=100, thumbnail_height=100)
        self.plan = Plan.objects.create()
        self.plan_with_access = Plan.objects.create(get_expiring_link=True)
        self.plan.size.add(self.tumbnail)
        self.userdetail = UserDetail.objects.create(
            user=self.user, plan=self.plan)
        self.userdetail_with_access = UserDetail.objects.create(
            user=self.user_with_access, plan=self.plan_with_access)
        self.file = UploadedFiles.objects.create(
            user=self.user, file_uploaded=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.file.plan.add(self.plan)

    def test_authorized_user_expire_without_plan(self):
        request = self.factory.get(reverse('resizer:expire-list'))
        force_authenticate(request, user=self.user)
        response = CreateExpiringLinkView.as_view(
            {'post': 'create'})(request)
        self.assertEqual(response.status_code, 403)

    # Need work, still got 405 error
    # def test_authorized_user_expire_with_plan(self):
    #     request = self.factory.get(
    #         reverse('resizer:expire-list'), {'user': self.user_with_access})
    #     force_authenticate(request, user=self.user_with_access)
    #     response = CreateExpiringLinkView.as_view(
    #         {'post': 'create'})(request)
    #     self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_expire_route(self):
        request = self.factory.get(reverse('resizer:expire-list'))
        response = CreateExpiringLinkView.as_view(
            {'post': 'create'})(request)
        self.assertEqual(response.status_code, 403)

    def test_create_expiring_link(self):
        request = self.factory.post(
            reverse('resizer:expire-list'), {'delayed_time': 1000, 'files': self.file})
        request.user = self.user_with_access
        force_authenticate(request, user=self.user_with_access)
        response = CreateExpiringLinkView.as_view(
            {'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)


class GetExpiringLinkTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.tumbnail = ThumbnailSize.objects.create(
            descriptive_name='test', thumbnail_width=100, thumbnail_height=100)
        self.plan = Plan.objects.create()
        self.plan.size.add(self.tumbnail)
        self.userdetail = UserDetail.objects.create(
            user=self.user, plan=self.plan)
        self.file = UploadedFiles.objects.create(
            user=self.user, file_uploaded=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        self.file.plan.add(self.plan)
        self.expire_link = ExpireLink.objects.create(
            delayed_time=2200, files=self.file)

    def test_authorized_user_expire_without_plan(self):
        request = self.factory.get(
            reverse('resizer:exlink-detail', kwargs={'pk': self.expire_link.id}))
        force_authenticate(request, user=self.user)
        response = GetExpiringLinkView.as_view(
            {'get': 'retrieve'})(request)
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_user_expire_route(self):
        request = self.factory.get(reverse('resizer:expire-list'))
        response = GetExpiringLinkView.as_view(
            {'get': 'retrieve'})(request)
        self.assertEqual(response.status_code, 403)
