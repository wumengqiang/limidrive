# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('file_id', models.IntegerField(serialize=False, primary_key=True)),
                ('file_name', models.CharField(max_length=100)),
                ('file_path', models.CharField(max_length=300)),
                ('file_type', models.CharField(max_length=20)),
                ('size', models.IntegerField()),
                ('last_modify', models.DateField(auto_now=True)),
                ('add_time', models.DateField(auto_now_add=True)),
                ('add_by', models.ForeignKey(related_name='add_set', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='owner_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
