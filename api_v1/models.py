# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    frequency = models.IntegerField(default=10, null=True)
    priority = models.IntegerField(default=3, null=True)
    next_reminder = models.DateField(default=timezone.now, null=True)
    last_contacted = models.DateField(default=timezone.now, null=True)
    notes = models.TextField(default="", null=True)
