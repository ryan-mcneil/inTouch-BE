# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from graphene.test import Client
from api_v1.models import Contact, ContactDetail, Occasion
from in_touch_be.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase
from snapshottest.django import TestCase as SnapshotTestCase

class ContactsTestCase(JSONWebTokenTestCase, SnapshotTestCase):
    fixtures = ['test_data']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.authenticate(self.user)

    def test_contacts_query(self):
        client = Client(schema)
        """Contacts query returns """
        query = '''
            query {
                contacts {
                    id
                    name
                    notes
                    frequency
                    priority
                    lastContacted
                    nextReminder
                    occasions {
                        id
                        description
                        date
                    }
                    contactDetails{
                        id
                        label
                        value
                    }
                }
            }
        '''
        response = self.client.execute(query)
        # import code; code.interact(local=dict(globals(), **locals()))
        self.assertMatchSnapshot(response.data)

    def test_contact_query(self):
        query = '''
            query {
                contact(id:1) {
                    name
                    notes
                    frequency
                    priority
                    lastContacted
                    nextReminder
                    occasions {
                        id
                        description
                        date
                    }
                    contactDetails{
                        id
                        label
                        value
                    }
                }
            }
        '''
        response = self.client.execute(query)
        self.assertMatchSnapshot(response.data)

class UserTestCase(JSONWebTokenTestCase, SnapshotTestCase):
    fixtures = ['test_data']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.authenticate(self.user)

    def test_create_user_mutation(self):
        client = Client(schema)
        """Contacts query returns """
        mutation = '''
            mutation {
                createUser(username:"Jamie Fox", email:"j@fox.com", password:"unchained"){
                    user {
                        id
                    }
                }
            }
        '''
        response = self.client.execute(mutation)
        self.assertMatchSnapshot(response.data)
