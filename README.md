[![Waffle.io - Columns and their card count](https://badge.waffle.io/ryan-mcneil/inTouch-BE.svg?columns=all)](https://waffle.io/ryan-mcneil/inTouch-BE)

Check out the frontend repo [here](https://github.com/Dhanciles/inTouch-FE)!

## Setup

Set up a python virtual environment where-ever you want it to live:
```

```

Next, set your DEBUG environment variable to True (for the virtual environment).
This lets you use a generic secret_key.
```
$ export DEBUG=True
```

Clone down the repo, activate the virtual environment, and install dependencies:
```
$ git clone git@github.com:ryan-mcneil/inTouch-BE.git
$ cd inTouch-BE
$ source <PATH_TO_VENV>/bin/activate
$ pip install -r requirements.txt
```


Next, set up a local database
```
$ psql
=# CREATE DATABASE in_touch_dev
```

## Making Requests

- All requests will be made to the endpoint `/api/v1/data`
- "query" and "variables" key-value pairs are sent in the body
- Authenticated endpoints must be sent with the header:

```json
"Authorization": "jwt %user-access-token%"
```
- Examples are formatted for readability. In practice, header and body values should be stripped of any line breaks. For example, for the query:

```
query {
  contacts {
    id
    name
  }
}
```
provide the following key-value pair:
```
"query": "query { contacts { id name } }"
```
### Queries
A query can be made for all of a user's contacts with any or all of the following attributes:
```
query {
  contacts {
    id
    name
    frequency
    priority
    nextReminder
    lastContacted
    notes
    contactDetails {
      id
      label
      value
      preferred
    }
  }
}
```
JSON Response (limited attributes):
```json
{
  "data": {
    "contacts": [
      {
        "id": "1",
        "name": "Mom",
        "contact_details": [
          {
            "label": "phone",
            "value": "123-456-7890",
            "preferred": true,
          }
        ]
      },
      {
        "id": "2",
        "name": "Dad"
      }
    ]
  }
}
```
A single contact can be queried with any of the same attributes:
```
query {
  contact(id: 1) {
    id
    name
    frequency
    priority
    nextReminder
    lastContacted
    notes
    contactDetails {
      id
      label
      value
      preferred
    }
  }
}
```
JSON Response (limited attributes):
```json
{
  "data": {
    "contact": {
      "id": "1",
      "name": "Mom",
      "contact_details": [
        {
          "label": "phone",
          "value": "123-456-7890",
        }
      ]
    }
  }
}
```
### Mutations

A contact can be created with a name (required) and any additional attributes with the following query:

```
mutation CreateContact($contactInput:ContactInput!) {
  createContact(input:$contactInput){
    ok
    contact {
      name
    }
  }
}
```
and variables:
```
{
  "contactInput": {
    "name": "Dad",
    "notes": "Some Notes"
  }
}
```
JSON Response:
```json
{
  "data": {
    "createContact": {
      "ok": true,
      "contact": {
        "name": "Dad"
      }
    }
  }
}
```

A contact can be updated by providing the contact id and any or all attributes with the following query:

```
mutation CreateContact($id:Int!, $contactInput:ContactInput!) {
  updateContact(id:$id, input:$contactInput){
    ok
    contact {
      name
    }
  }
}
```
and variables:
```
{
  "contactInput": {
    "name": "Father",
    "priority": "3",
    "lastContacted": "2019-03-02",
    "notes": "Some New Notes",
  },
  "id": 3
}
```
JSON Response:
```json
{
  "data": {
    "updateContact": {
      "ok": true,
      "contact": {
        "name": "Father"
      }
    }
  }
}
```
A contact can be deleted by providing the contact id with the following query:


```
mutation DeleteContact($id:Int!) {
  deleteContact(id:$id){
    ok
  }
}
```
and variables:
```
{
  "id": 3
}
```
JSON Response:
```json
{
  "data": {
    "deleteContact": {
      "ok": true,
    }
  }
}
```
