# Importing the libraries
from graphene_django import DjangoObjectType

from ema import models


class UsersType(DjangoObjectType):
    """
    Defining the Userstype
    """
    class Meta:
        """
        Inner class for setting the model
        to Users
        """
        model=models.Users


class MeetingType(DjangoObjectType):
    """
    Definition Meeting Type
    """
    class Meta:
        """
        Inner class for setting the model
        to Meeting
        """
        model=models.Meeting
        

class CommentType(DjangoObjectType):
    """
    Definition Comment Type
    """
    class Meta:
        """
        Inner class for setting the model
        to Comment
        """
        model=models.Comment


class OTPType(DjangoObjectType):
    """
    Definition OTP Type
    """
    class Meta:
        """
        Inner class for setting the model
        to OTP
        """
        model = models.OTP
        