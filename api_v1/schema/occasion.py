from .schema_helper import *

class OccasionType(DjangoObjectType):
    class Meta:
        model = Occasion

# class OccasionInput(graphene.InputObjectType):
#     id = graphene.ID()
#     description = graphene.String(required=True)
#     frequency = graphene.Int()
#     priority = graphene.Int()
#     next_reminder = graphene.types.datetime.Date()
#     last_contacted = graphene.types.datetime.Date()
#     notes = graphene.String()

class OccasionFields(graphene.AbstractType):
    description = graphene.String()
    date = graphene.types.datetime.Date()

class CreateOccasionInput(graphene.InputObjectType, OccasionFields):
    description = graphene.String(required=True)
    date = graphene.types.datetime.Date(required=True)

class UpdateOccasionInput(graphene.InputObjectType, OccasionFields):
    pass

class CreateOccasion(graphene.Mutation):
    Output = OccasionType
    class Arguments:
        contact_id = graphene.Int(required = True)
        input = CreateOccasionInput(required = True)

    @staticmethod
    @login_required
    def mutate(root, info, contact_id, input = None):

        user = info.context.user
        contact_instance = Contact.objects.get(pk=contact_id, user_id=user.id)
        if contact_instance:
            occasion_instance = Occasion()
            for key in input:
                setattr(occasion_instance, key, input[key])
            occasion_instance.contact_id = contact_instance.id
            occasion_instance.save()
            return occasion_instance
        return None

class Mutation(graphene.ObjectType):
    create_occasion = CreateOccasion.Field()
