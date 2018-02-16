# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-16 20:51
from __future__ import unicode_literals

from django.db import migrations
import osf.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('addons_wiki', '0007_auto_20180124_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipage',
            name='date',
        ),
        migrations.RemoveField(
            model_name='wikipage',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='wikiversion',
            name='date',
        ),
        migrations.AddField(
            model_name='wikipage',
            name='deleted',
            field=osf.utils.fields.NonNaiveDateTimeField(blank=True, null=True),
        ),
    ]
