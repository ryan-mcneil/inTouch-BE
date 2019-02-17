from .schema_helper import *

class ContactDetailType(DjangoObjectType):
    class Meta:
        model = ContactDetail
