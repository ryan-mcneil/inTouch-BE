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

class UpdateContactDetailInput(graphene.InputObjectType, ContactDetailFields):
    pass

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

class UpdateContactDetail(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UpdateContactDetailInput(required=True)

    contact_detail = graphene.Field(ContactDetailType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        user = info.context.user
        contact_detail_instance = ContactDetail.objects.get(pk=id)
        contact_instance = Contact.objects.get(pk=contact_detail_instance.contact_id, user_id=user.id)
        if contact_instance and contact_detail_instance:
            for key in input:
                setattr(contact_detail_instance, key, input[key])
            contact_detail_instance.save()
            return UpdateContactDetail(contact_detail=contact_detail_instance)
        return None

class DeleteContactDetail(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    contact_detail = graphene.Field(ContactDetailType)
    ok = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, id):
        user = info.context.user
        ok = False
        contact_detail_instance = ContactDetail.objects.get(pk=id)
        contact_instance = Contact.objects.get(pk=contact_detail_instance.contact_id, user_id=user.id)
        if contact_instance and contact_detail_instance:
            ok = True
            contact_detail_instance.delete()
            return DeleteContactDetail(ok=ok)
        return DeleteContactDetail(ok=ok)


class Mutation(graphene.ObjectType):
    create_contact_detail = CreateContactDetail.Field()
    update_contact_detail = UpdateContactDetail.Field()
    delete_contact_detail = DeleteContactDetail.Field()
