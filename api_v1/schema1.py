import graphene

from graphene_django.types import DjangoObjectType, ObjectType
from api_v1.models import Contact
from django.contrib.auth.models import User
from rest_framework.authentication import get_authorization_header
from graphql_jwt.decorators import login_required


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(ObjectType):
    contact = graphene.Field(ContactType, id=graphene.Int())
    contacts = graphene.List(ContactType)

    @login_required
    def resolve_contact(self, info, **kwargs):
        user = info.context.user
        contact_id = kwargs.get('id')
        if contact_id is not None:
            return Contact.objects.get(pk=contact_id, user_id=user.id)
        return None

    @login_required
    def resolve_contacts(self, info, **kwargs):
        user = info.context.user
        return Contact.objects.filter(user_id=user.id)

class ContactInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    frequency = graphene.Int()
    priority = graphene.Int()
    next_reminder = graphene.types.datetime.Date()
    last_contacted = graphene.types.datetime.Date()
    notes = graphene.String()

class CreateContact(graphene.Mutation):
    class Arguments:
        input = ContactInput(required=True)

    ok = graphene.Boolean()
    contact = graphene.Field(ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        user = info.context.user
        ok = True
        contact_instance = Contact(
            id = input.id,
            name = input.name,
            frequency = input.frequency,
            priority = input.priority,
            next_reminder = input.next_reminder,
            last_contacted = input.last_contacted,
            notes = input.notes,
        )
        contact_instance.user_id = user.id
        contact_instance.save()
        return CreateContact(ok=ok, contact=contact_instance)

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
    create_user = CreateUser.Field()
