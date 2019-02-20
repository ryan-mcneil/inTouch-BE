import graphene

from graphene_django.types import DjangoObjectType, ObjectType
from django.contrib.auth.models import User
from rest_framework.authentication import get_authorization_header
from graphql_jwt.decorators import login_required
from api_v1.models import Contact, ContactDetail, Occasion
from datetime import datetime, timedelta
