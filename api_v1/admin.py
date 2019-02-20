# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api_v1.models import Contact, ContactDetail, Occasion

admin.site.register(Contact)
admin.site.register(ContactDetail)
admin.site.register(Occasion)
