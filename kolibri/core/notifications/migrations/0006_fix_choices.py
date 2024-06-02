# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-11-21 15:03
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0005_learnerprogressnotification_assignment_collections"),
    ]

    operations = [
        migrations.AlterField(
            model_name="learnerprogressnotification",
            name="notification_event",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Answered", "Answered"),
                    ("Completed", "Completed"),
                    ("HelpNeeded", "Help"),
                    ("Started", "Started"),
                ],
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="learnerprogressnotification",
            name="reason",
            field=models.CharField(
                blank=True,
                choices=[("MultipleUnsuccessfulAttempts", "Multiple")],
                max_length=200,
            ),
        ),
    ]
