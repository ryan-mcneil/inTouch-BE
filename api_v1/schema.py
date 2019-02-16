import graphene

from graphene_django.types import DjangoObjectType, ObjectType
from api_v1.models import Contact

class ContactType(DjangoObjectType):
    class Meta:
        model = Contact

class Query(ObjectType):
    contact = graphene.Field(ContactType, id=graphene.Int())
    contacts = graphene.List(ContactType)

    def resolve_contact(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Contact.objects.get(pk=id)
        return None

    def resolve_contacts(self, info, **kwargs):
        return Contact.objects.all()

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
    def mutate(root, info, input=None):
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
        contact_instance.user_id = 2
        contact_instance.save()
        return CreateContact(ok=ok, contact=contact_instance)

class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
