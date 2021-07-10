# Generated by Django 3.2.5 on 2021-07-06 11:50

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0004_rename_uploadedfiels_uploadedfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfiles',
            name='post_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=0, size=[50, 50], upload_to='pictures/%Y/%m/%d/'),
        ),
    ]