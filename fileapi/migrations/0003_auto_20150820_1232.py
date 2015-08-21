# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileapi', '0002_auto_20150820_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='last_modify',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
