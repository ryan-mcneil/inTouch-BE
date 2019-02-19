from .schema_helper import *

class ContactDetailType(DjangoObjectType):
    class Meta:
        model = ContactDetail

class ContactDetailFields(graphene.AbstractType):
    label = graphene.String()
    value = graphene.String()
    preferred = graphene.Boolean()

class CreateContactDetailInput(graphene.InputObjectType, ContactDetailFields):
    label = graphene.String(required=True)
    value = graphene.String(required=True)

class CreateContactDetail(graphene.Mutation):
    class Arguments:
        contact_id = graphene.Int(required = True)
        input = CreateContactDetailInput(required=True)

    contact_detail = graphene.Field(ContactDetailType)

    @staticmethod
    @login_required
    def mutate(root, info, contact_id, input=None):
        user = info.context.user
        contact_instance = Contact.objects.get(pk=contact_id, user_id=user.id)
        if contact_instance:
            contact_detail_instance = ContactDetail()
            for key in input:
                setattr(contact_detail_instance, key, input[key])
            if len(ContactDetail.objects.filter(contact_id=contact_instance.id)) == 0:
                contact_detail_instance.preferred = True
            contact_detail_instance.contact_id = contact_instance.id
            contact_detail_instance.save()
            return CreateContactDetail(contact_detail=contact_detail_instance)
        return None

class Mutation(graphene.ObjectType):
    create_contact_detail = CreateContactDetail.Field()
