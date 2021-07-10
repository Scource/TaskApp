# Generated by Django 3.2.5 on 2021-07-07 06:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0012_expirelink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expirelink',
            name='delay',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(3000)]),
        ),
    ]
