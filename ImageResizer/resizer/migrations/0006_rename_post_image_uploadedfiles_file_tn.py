# Generated by Django 3.2.5 on 2021-07-06 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0005_uploadedfiles_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadedfiles',
            old_name='post_image',
            new_name='file_tn',
        ),
    ]
