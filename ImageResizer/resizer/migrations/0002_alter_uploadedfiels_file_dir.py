# Generated by Django 3.2.5 on 2021-07-06 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfiels',
            name='file_dir',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='pictures/%Y/%m/%d/'),
        ),
    ]
