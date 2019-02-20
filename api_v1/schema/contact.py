from .schema_helper import *

class ContactType(DjangoObjectType):
    class Meta:
        model = Contact

class Query(ObjectType):
    contact = graphene.Field(ContactType, id=graphene.Int())
    contacts = graphene.List(ContactType)
    contact_suggestions = graphene.List(ContactType, lead_time=graphene.Int())

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

    def resolve_contact_suggestions(self, info, **kwargs):
        user = info.context.user
        days = kwargs.get('lead_time', 7)
        now = datetime.now()
        later_date = now + timedelta(days)

        contacts =  Contact.objects.filter(next_reminder__lt=later_date, user_id=user.id)

        return contacts.order_by('next_reminder', 'priority')

class ContactFields(graphene.AbstractType):
    name = graphene.String()
    frequency = graphene.Int()
    priority = graphene.Int()
    next_reminder = graphene.types.datetime.Date()
    last_contacted = graphene.types.datetime.Date()
    notes = graphene.String()

class CreateContactInput(graphene.InputObjectType, ContactFields):
    name = graphene.String(required=True)

class UpdateContactInput(graphene.InputObjectType, ContactFields):
    pass

class CreateContact(graphene.Mutation):
    class Arguments:
        input = CreateContactInput(required=True)

    ok = graphene.Boolean()
    contact = graphene.Field(ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        user = info.context.user
        ok = True
        contact_instance = Contact()
        for key in input:
            setattr(contact_instance, key, input[key])
        contact_instance.next_reminder = contact_instance.last_contacted + timedelta(contact_instance.frequency)
        contact_instance.user_id = user.id
        contact_instance.save()
        return CreateContact(ok=ok, contact=contact_instance)

class UpdateContact(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UpdateContactInput(required=True)

    ok = graphene.Boolean()
    contact = graphene.Field(ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        user = info.context.user
        ok = False
        contact_instance = Contact.objects.get(pk=id)
        if contact_instance and user.id == contact_instance.user_id:
            ok = True

            for key in input:
                setattr(contact_instance, key, input[key])
            if input.last_contacted:
                contact_instance.next_reminder = contact_instance.last_contacted + timedelta(contact_instance.frequency)
            contact_instance.save()
            return UpdateContact(ok=ok, contact=contact_instance)
        return UpdateContact(ok=ok, contact=None)

class DeleteContact(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, id):
        user = info.context.user
        ok = False
        contact_instance = Contact.objects.get(pk=id)
        if contact_instance and user.id == contact_instance.user_id:
            ok = True
            contact_instance.delete()
            return DeleteContact(ok=ok)
        return DeleteContact(ok=ok)

class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
    update_contact = UpdateContact.Field()
    delete_contact = DeleteContact.Field()
