from django.db import models
from django.conf import settings
from django.core.validators import *

# Create your models here.


class ThumbnailSize(models.Model):
    '''Defines possible thumbnail sizes'''
    descriptive_name = models.CharField(
        max_length=25, validators=[MinLengthValidator(3), MaxLengthValidator(25)])
    thumbnail_width = models.PositiveIntegerField(
        validators=[MinValueValidator(28), MaxValueValidator(2048)])
    thumbnail_height = models.PositiveIntegerField(
        validators=[MinValueValidator(28), MaxValueValidator(2048)])

    def __str__(self):
        return self.descriptive_name


class Plan(models.Model):
    '''Defines Plans properties'''
    name = models.CharField(max_length=25, validators=[
                            MinLengthValidator(3), MaxLengthValidator(25)])
    size = models.ManyToManyField(ThumbnailSize)
    get_origial = models.BooleanField(default=False)
    get_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserDetail(models.Model):
    '''Extends users model with Plan data'''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username


class UploadedFiles(models.Model):
    '''Stores files uplaoded by users and created thumbnails'''
    added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_uploaded = models.ImageField(
        upload_to='images/%Y%m%d/', max_length=255, null=True, blank=True)
    original = models.BooleanField(default=True)
    plan = models.ManyToManyField(Plan)

    @classmethod
    def create_new_thumbnail(cls, data):
        new_tnail = UploadedFiles.objects.create(**data)
        return new_tnail

    @classmethod
    def add_plan_to_file(cls, plans, file):
        file.plan.add(plans)

    def __str__(self):
        return self.file_uploaded.name

    class Meta:
        verbose_name_plural = "Uploaded files"


class ExpireLink(models.Model):
    '''Stores data needed to create expiring links'''
    generated = models.DateTimeField(null=True)
    delayed_time = models.PositiveIntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(30000)])
    expire_time = models.DateTimeField(null=True)
    files = models.ForeignKey(UploadedFiles, on_delete=models.DO_NOTHING)
