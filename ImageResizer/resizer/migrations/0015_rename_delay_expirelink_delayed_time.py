# Generated by Django 3.2.5 on 2021-07-07 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0014_alter_expirelink_delay'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expirelink',
            old_name='delay',
            new_name='delayed_time',
        ),
    ]
