# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['ContactsTestCase::test_contact_query 1'] = {
    'contact': {
        'contactDetails': [
        ],
        'frequency': 12,
        'lastContacted': '2019-02-20',
        'name': 'Monty',
        'nextReminder': '2019-02-20',
        'notes': "I've got a lovely bunch of coconuts.",
        'occasions': [
        ],
        'priority': 1
    }
}

snapshots['ContactsTestCase::test_contacts_query 1'] = {
    'contacts': [
        {
            'contactDetails': [
            ],
            'frequency': 12,
            'id': '1',
            'lastContacted': '2019-02-20',
            'name': 'Monty',
            'nextReminder': '2019-02-20',
            'notes': "I've got a lovely bunch of coconuts.",
            'occasions': [
            ],
            'priority': 1
        },
        {
            'contactDetails': [
            ],
            'frequency': 18,
            'id': '2',
            'lastContacted': '2019-02-20',
            'name': 'Python',
            'nextReminder': '2019-02-20',
            'notes': "I'll bite your leg off!",
            'occasions': [
            ],
            'priority': 3
        },
        {
            'contactDetails': [
            ],
            'frequency': 2,
            'id': '3',
            'lastContacted': '2019-02-20',
            'name': 'Pepperpots',
            'nextReminder': '2019-02-20',
            'notes': 'She turned me into a newt!',
            'occasions': [
            ],
            'priority': 5
        },
        {
            'contactDetails': [
            ],
            'frequency': 9,
            'id': '4',
            'lastContacted': '2019-02-20',
            'name': 'The Knights',
            'nextReminder': '2019-02-20',
            'notes': 'Ni.',
            'occasions': [
            ],
            'priority': 2
        },
        {
            'contactDetails': [
            ],
            'frequency': 100,
            'id': '5',
            'lastContacted': '2019-02-20',
            'name': 'Mr. Badger',
            'nextReminder': '2019-02-20',
            'notes': "I won't ruin your sketch.",
            'occasions': [
            ],
            'priority': 4
        }
    ]
}

snapshots['UserTestCase::test_create_user_mutation 1'] = {
    'createUser': {
        'user': {
            'id': '2'
        }
    }
}
