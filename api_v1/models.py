# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    frequency = models.IntegerField(default=10)
    priority = models.IntegerField(default=3)
    next_reminder = models.DateField(timezone.now)
    last_contacted = models.DateField(timezone.now)
    notes = models.TextField(default="")
