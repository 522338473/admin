# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-27 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='recv_date',
            field=models.DateField(blank=True, null=True, verbose_name='接客时间'),
        ),
    ]
