from .schema_helper import *
from api_v1.schema.contact import ContactType
from datetime import datetime, timedelta
from calendar import monthrange
from functools import reduce
from django.db.models.functions import Extract, Cast
from django.db.models import F, IntegerField
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

        # Get number of days in current month
        _, days_in_month = monthrange(now.year, now.month)

        ### Solution for querying credited to "twneale"
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

        # Query for matching monthday pairs for the authorized user.
        occasions = Occasion.objects.filter(query, contact__user_id=user.id)

        # Extract the day and month fields as integers
        occasions = occasions.annotate(month=Cast(Extract('date','month'), IntegerField()),day=Cast(Extract('date','day'), IntegerField()))

        # Order by "time from now", evaluate expression, and return
        return occasions.order_by(((F('month') - now.month)+12) % 12, 'day')


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
    ok = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, contact_id, input = None):
        ok = False
        user = info.context.user
        contact_instance = Contact.objects.filter(pk=contact_id, user_id=user.id)
        if contact_instance:
            ok = True
            contact_instance = contact_instance[0]
            occasion_instance = Occasion()
            for key in input:
                setattr(occasion_instance, key, input[key])
            occasion_instance.contact_id = contact_instance.id
            occasion_instance.save()
            return CreateOccasion(ok = ok, occasion=occasion_instance)
        return CreateOccasion(ok = ok)

class UpdateOccasion(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UpdateOccasionInput(required=True)

    ok = graphene.Boolean()
    occasion = graphene.Field(OccasionType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        user = info.context.user
        ok = False
        occasion_instance = Occasion.objects.filter(pk=id, contact__user_id = user.id)
        if occasion_instance:
            ok = True
            for key in input:
                setattr(occasion_instance[0], key, input[key])
            occasion_instance.save()
            return UpdateOccasion(ok=ok, occasion=occasion_instance[0])
        return UpdateOccasion(ok=ok, occasion=None)

class DeleteOccasion(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, id):
        user = info.context.user
        ok = False
        occasion = Occasion.objects.filter(pk=id, contact__user_id = user.id)
        if occasion:
            occasion.delete()
            ok = True
        return UpdateOccasion(ok=ok)

class Mutation(graphene.ObjectType):
    create_occasion = CreateOccasion.Field()
    update_occasion = UpdateOccasion.Field()
    delete_occasion = DeleteOccasion.Field()
