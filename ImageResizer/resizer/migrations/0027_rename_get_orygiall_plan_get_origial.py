# Generated by Django 3.2.5 on 2021-07-08 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0026_auto_20210708_1919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='get_orygiall',
            new_name='get_origial',
        ),
    ]
