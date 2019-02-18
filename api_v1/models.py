# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    frequency = models.IntegerField(default=10)
    priority = models.IntegerField(default=3)
    next_reminder = models.DateField(default=timezone.now)
    last_contacted = models.DateField(default=timezone.now)
    notes = models.TextField(default="")

class ContactDetail(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_details')
    label = models.TextField()
    value = models.TextField()
    preferred = models.BooleanField(default=False)

class Occasion(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='occasions')
    description = models.TextField()
    date = models.DateField()
