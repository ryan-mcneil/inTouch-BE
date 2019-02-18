[![Waffle.io - Columns and their card count](https://badge.waffle.io/ryan-mcneil/inTouch-BE.svg?columns=all)](https://waffle.io/ryan-mcneil/inTouch-BE)

@import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false}
<!-- code_chunk_output -->

* [Description](#description)
* [API Documentation](#api-documentation)
	* [Making Requests](#making-requests)
		* [Request Formatting](#request-formatting)
		* [User Creation and Authentication](#user-creation-and-authentication)
			* [Create a New User](#create-a-new-user)
			* [Authenticate an existing user](#authenticate-an-existing-user)
			* [Authorize a Request](#authorize-a-request)
		* [Queries](#queries)
			* [Contacts](#contacts)
			* [Single Contact](#single-contact)
		* [Mutations](#mutations)
			* [Create Contact](#create-contact)
			* [Update Contact](#update-contact)
			* [Delete Contact](#delete-contact)
* [For Contributors](#for-contributors)
	* [Backend Tech Stack](#backend-tech-stack)
	* [Getting Started](#getting-started)
	* [Setup](#setup)
	* [Core Team](#core-team)

<!-- /code_chunk_output -->

# Description

If you're like most people, it's getting harder and harder to create and nurture deep, meaningful relationships as we transfer our social lives to digital media. If you're like most people, you want to do something about it.

**InTouch** is a minimalist app designed to help you stay connected with people you care about. It's not a social media network or an automated communications system. You don't set it and forget it. It's more like a friend who reminds you to reach out to your loved ones now and then in meaningful ways.

This is the **official backend application for InTouch.**
Check out the frontend repo [here](https://github.com/Dhanciles/inTouch-FE)!

# API Documentation

## Making Requests
### Request Formatting
- Because it's a GraphQL API, all requests should be POST requests
- All requests are sent to the endpoint `/api/v1/data`
- "query" and "variables" key-value pairs are sent in the body

Examples are formatted for readability. In practice, header and body values should be stripped of any line breaks. For example, for the query:
```graphql
query {
  contacts {
    id
    name
  }
}
```
Send the following JSON formatted key/value pair:
```json
{ "query": "query { contacts { id name } }" }
```
The same is true for mutations.
```json
{ "query": "mutation {... }" }
```
And if you need to send variables with the request:
```json
{
  "query": "mutation CreateTestContact($contactInput: ContactInput!){ createContact(input:$contactInput){ ok contact { name } } }",
  "variables": "{ \"contactInput\": {\"frequency\": 10, \"name\": \"Joey\"} }"
}
```
### User Creation and Authentication
This app is secured using Django's default user authentication and JSON Web Tokens (JWT).



#### Create a New User
Send a `createUser` request to create a new user account:
```graphql
mutation {
  createUser(email:"me@me.com", username:"myself", password:"mypassword"){
    user{
      username
    }
  }
}
```
#### Authenticate an existing user
When an account has been created, send a `tokenAuth` request to authenticate the user and get a JWT:
```graphql
mutation {
  tokenAuth(username:"myself", password:"myself"){
    token
  }
}
```
This will return :
```json
{
  "data": {
    "tokenAuth": {
      "token": "%user-access-token%"
    }
  }
}
```
This token is used for `Authorization` of future requests.

#### Authorize a Request
Endpoints requiring authorization (i.e. the rest of then) must be sent with the header:
```json
"Authorization": "JWT %user-access-token%"
```

### Queries
All queries are scoped to the user making the request, which is determined by the JWT sent in the `Authorization` header.
#### Contacts
A query can be made for all of a user's contacts with any or all of the following attributes:
```graphql
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
#### Single Contact
A single contact can be queried with any of the same attributes:
```graphql
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
#### Create Contact
A contact can be created with a name (required) and any additional attributes with the following query:

```graphql
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
```json
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
#### Update Contact
A contact can be updated by providing the contact id and any or all attributes with the following query:

```graphql
mutation UpdateContact($id:Int!, $contactInput:ContactInput!) {
  updateContact(id:$id, input:$contactInput){
    ok
    contact {
      name
    }
  }
}
```
and variables:
```json
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
#### Delete Contact
A contact can be deleted by providing the contact id with the following query:
```graphql
mutation DeleteContact($id:Int!) {
  deleteContact(id:$id){
    ok
  }
}
```
and variables:
```json
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

# For Contributors
## Backend Tech Stack
  - Django 2.1.7
  - Python 3.2.7
  - GraphQL with Graphene

## Getting Started
This is an ongoing OpenSource project that we want to make as useful as possible without experiencing feature bloat. Contributions are welcome and encouraged! To make it as easy as possible for future contributors, we're committed to keeping our test-coverage high and our tech-debt low, so pull requests will be thoroughly reviewed and vetted before merging.

## Setup

Set up a python virtual environment where-ever you want it to live:
```

```

Next, set your DEBUG environment variable to True (for the virtual environment).
This lets you use a generic secret_key.
```bash
$ export DEBUG=True
```

Clone down the repo, activate the virtual environment, and install dependencies:
```bash
$ git clone git@github.com:ryan-mcneil/inTouch-BE.git
$ cd inTouch-BE
$ source <PATH_TO_VENV>/bin/activate
$ pip install -r requirements.txt
```


Next, set up a local database
```bash
$ psql
=> CREATE DATABASE in_touch_dev
```

## Core Team
Ryan McNeil
William Fischer
Rajaa
