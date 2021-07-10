# Generated by Django 3.2.5 on 2021-07-07 14:59

from django.db import migrations
import django.utils.timezone
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0018_alter_expirelink_generated'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfiles',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(default=django.utils.timezone.now, upload_to='avatars'),
            preserve_default=False,
        ),
    ]