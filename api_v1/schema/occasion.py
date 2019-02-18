from .schema_helper import *
from api_v1.schema.contact import ContactType
from datetime import datetime, timedelta
from functools import reduce
import operator

from django.db.models import Q

class OccasionType(DjangoObjectType):
    class Meta:
        model = Occasion

class Query(graphene.ObjectType):
    upcoming_occasions = graphene.List(OccasionType, lead_time=graphene.Int())

    @login_required
    def resolve_upcoming_occasions(self, info, **kwargs):
        user = info.context.user
        days = kwargs.get('lead_time', 7)
        now = datetime.now()
        then = now + timedelta(days)

        ### Solution credited to "twneale"
        # I get it, but I wouldn't have thought of it.
        # https://stackoverflow.com/questions/6128921/queryset-of-people-with-a-birthday-in-the-next-x-days

        # Build the list of month/day tuples.
        monthdays = [(now.month, now.day)]
        while now <= then:
            monthdays.append((now.month, now.day))
            now += timedelta(days=1)

        monthdays = (dict(zip(("date__month", "date__day"), t))
            for t in monthdays)

        # Compose the djano.db.models.Q objects together for a single query.
        query = reduce(operator.or_, (Q(**d) for d in monthdays))
        return Occasion.objects.filter(query, contact__user_id=user.id)

class OccasionFields(graphene.AbstractType):
    description = graphene.String()
    date = graphene.types.datetime.Date()

class CreateOccasionInput(graphene.InputObjectType, OccasionFields):
    description = graphene.String(required=True)
    date = graphene.types.datetime.Date(required=True)

class UpdateOccasionInput(graphene.InputObjectType, OccasionFields):
    pass

class CreateOccasion(graphene.Mutation):
    class Arguments:
        contact_id = graphene.Int(required = True)
        input = CreateOccasionInput(required = True)

    occasion = graphene.Field(OccasionType)
    contact = graphene.Field(ContactType)

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
            return CreateOccasion(occasion=occasion_instance, contact=contact_instance)
        return None

class Mutation(graphene.ObjectType):
    create_occasion = CreateOccasion.Field()
