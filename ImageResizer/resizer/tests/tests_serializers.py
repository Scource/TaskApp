from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from ..models import *
from django.contrib.auth.models import User
from ..views import *
import tempfile
from ..serializers import *
import datetime
from dateutil import parser


class UploadedFileSerializerTest(TestCase):
    def setUp(self):

        tmp1 = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.file = {
            'user': User.objects.create_user(
                username='test', email='test@test.com', password='test'),
            'file_uploaded': tmp1
        }

        self.uploadedfile = UploadedFiles.objects.create(**self.file)
        self.serializer = UploadedFileSerializer(instance=self.uploadedfile)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), ['user', 'file_uploaded', 'added'])

    def test_user_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.uploadedfile.user.id)

    def test_file_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['file_uploaded'],
                         '/media'+self.uploadedfile.file_uploaded.name)

    def test_added_field_content(self):
        data = self.serializer.data
        self.assertAlmostEqual(parser.parse(
            data['added'], ignoretz=True), datetime.datetime.now(), delta=datetime.timedelta(1000))


class ExpireLinkSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        factory = APIRequestFactory()
        self.request = factory.post('/')
        self.request.user = self.user
        tmp1 = tempfile.NamedTemporaryFile(suffix=".jpg").name
        self.file = {
            'user': self.user,
            'file_uploaded': tmp1
        }
        self.uploadedfile = UploadedFiles.objects.create(**self.file)

        self.link_data = {
            'files': self.uploadedfile,
            'delayed_time': 2000,
            'expire_time': datetime.datetime.now()+datetime.timedelta(seconds=int(2000))
        }

        self.link = ExpireLink.objects.create(**self.link_data)
        self.serializer = ExpireLinkSerializer(
            instance=self.link, context={'request': self.request})

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), ['files', 'delayed_time', 'expire_time'])

    def test_files_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['files'],
                         self.link.files.id)

    def test_files_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['delayed_time'],
                         self.link.delayed_time)

    def test_delayed_time_field_content(self):
        data = self.serializer.data
        self.assertAlmostEqual(parser.parse(
            data['expire_time'], ignoretz=True), self.link.expire_time, delta=datetime.timedelta(1000))
