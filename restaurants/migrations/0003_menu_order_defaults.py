# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-03 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_menu_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]