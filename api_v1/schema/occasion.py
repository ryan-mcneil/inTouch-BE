from .schema_helper import *

class OccasionType(DjangoObjectType):
    class Meta:
        model = Occasion
