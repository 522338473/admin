# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_remove_iport_creat_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='iport',
            name='creat_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='时间'),
        ),
    ]
