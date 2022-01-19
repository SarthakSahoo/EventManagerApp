#Importing the libraries
from graphene import relay

from graphene_django import DjangoObjectType

from ema.models import Meeting


class MeetingNode(DjangoObjectType):
    """
    Defining the class to map Meeting model into
    the Meeting node. This is configured in the 
    MeetingNode Meta class.
    """
    class Meta:
        # Specifing the Meeting model 
        model=Meeting

        # Defining the filter field with the condition
        filter_fields={
            'date': ['gt']
        }
        interfaces=(relay.Node, )
        