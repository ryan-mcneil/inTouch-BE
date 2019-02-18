from .schema_helper import *

class ContactType(DjangoObjectType):
    class Meta:
        model = Contact

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
        contact_instance = Contact()
        for key in input:
            setattr(contact_instance, key, input[key])
            
        contact_instance.user_id = user.id
        contact_instance.save()
        return CreateContact(ok=ok, contact=contact_instance)

class UpdateContact(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ContactInput(required=True)

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

            # add the following once implemented
            # contact_details = []
            # occasions = []

            for key in input:
                setattr(contact_instance, key, input[key])

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
