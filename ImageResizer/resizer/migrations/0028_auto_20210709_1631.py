# Generated by Django 3.2.5 on 2021-07-09 14:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resizer', '0027_rename_get_orygiall_plan_get_origial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='user',
        ),
        migrations.AddField(
            model_name='uploadedfiles',
            name='original',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='expirelink',
            name='delayed_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)]),
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='resizer.plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
