# Generated by Django 3.2.5 on 2021-07-06 10:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resizer', '0003_auto_20210706_1031'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UploadedFiels',
            new_name='UploadedFiles',
        ),
    ]
