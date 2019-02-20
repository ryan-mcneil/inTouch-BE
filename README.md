[![Waffle.io - Columns and their card count](https://badge.waffle.io/ryan-mcneil/inTouch-BE.svg?columns=all)](https://waffle.io/ryan-mcneil/inTouch-BE)

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
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
			* [Suggested Contacts](#suggested-contacts)
		* [Mutations](#mutations)
			* [Create Contact](#create-contact)
			* [Update Contact](#update-contact)
			* [Delete Contact](#delete-contact)
* [For Contributors](#for-contributors)
	* [Backend Tech Stack](#backend-tech-stack)
	* [Getting Started](#getting-started)
	* [Setup](#setup)
	* [Pull Requests](#pull-requests)
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
A single contact with id = 1 can be queried with any of the same attributes:
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
JSON Response (limited attributes shown):
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
#### Suggested Contacts
A query can be made for suggested contacts, determined by nextReminder and priority, for a user specified leadTime = 7 (days), with any or all of the following attributes:
```graphql
query {
  contactSuggestions(leadTime: 7) {
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
		occasions {
			id
			description
			date
		}
  }
}
```
JSON Response (limited attributes shown):
```json
{
  "data": {
    "contactSuggestions": [
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
  - Django v2.1.7
  - Python v3.2.7
  - GraphQL with Graphene v2.1.3
  - PostgreSQL v11.1

## Getting Started
This is an ongoing OpenSource project that we want to make as useful as possible without experiencing feature bloat. Contributions are welcome and encouraged! To make it as easy as possible for future contributors, we're committed to keeping our test-coverage high and our tech-debt low, so pull requests will be thoroughly reviewed and vetted before merging.

## Setup

Set up a virtual debug environment where-ever you want it to live, then activate it:
```bash
$ python3 -m venv $PATH_TO_VENV/dj-env
$ echo "export DEBUG=True" >> $PATH_TO_VENV/dj-env/postactivate
$ source <PATH_TO_VENV>/bin/activate

```
We like to make a `dj-env` for Django specifically. The second command creates a script to run after the virtual environment is activated. You can also set up Django specific bash aliases in this file.

The `DEBUG=True` is used in `settings.py` to use a generic secret_key for local development.

Next, clone down the repo and install dependencies:
```bash
$ git clone git@github.com:ryan-mcneil/inTouch-BE.git
$ cd inTouch-BE
$ pip install -r requirements.txt
```
Set up a local database:
```bash
$ psql
=> CREATE DATABASE in_touch_dev
```
Then run migrations:
```bash
$ python manage.py migrate
```
Now you should be able to run the server locally:
```
$ python manage.py runserver
```
Visit http://localhost:8000/api/v1/data to interact using the GraphiQL GUI and view the schema documentation.
We recommend creating a superuser for your local server:
```bash
$ python manage.py createsuperuser
```
After that, you can visit http://localhost:8000/admin and log in. The admin account you log in as will be used for authenticating any requests made through the GraphiQL interface. To directly manipulate the authorization header, we recommend using [Insomnia](https://insomnia.rest/download/#mac), which was designed with GraphQL in mind. [Postman](https://www.getpostman.com/) is an excellent choice also.

## Pull Requests
When you make changes you want to incorporate, please submit a PR to the `dev` branch. We have a live staging deployment on Heroku that we use to check new functionality and compatibility before deploying to master and deploying to production. (At the moment, we actually don't have a production deployment, but we will soon!)

## Core Team
* [Ryan McNeil](https://github.com/ryan-mcneil)
* [William Fischer](https://github.com/wfischer42)
* [Rajaa Boulassouak](https://github.com/RajaaBoulassouak)
* [Derek Hanciles](https://github.com/Dhanciles)
