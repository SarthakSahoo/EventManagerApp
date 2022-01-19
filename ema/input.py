# Importing the libraries
import graphene

class UsersInput(graphene.InputObjectType):
    """
    Input for Users in Graphene backend.
    Type: graphene.InputObjectType
    """

    # ID field
    id=graphene.ID()

    # String Fields
    email=graphene.String()
    first_name=graphene.String()
    last_name=graphene.String()
    password=graphene.String()


class MeetingInput(graphene.InputObjectType):
    """
    Input for Meeting in Graphene backend.
    Type: graphene.InputObjectType
    """

    # ID field
    id=graphene.ID()

    # Date and Time fields
    date=graphene.Date()
    time=graphene.Time()

    # String fields
    description=graphene.String()
    title=graphene.String()
    
    # Input of type List UsersInput
    # Which references to the above class
    joinee=graphene.List(UsersInput)


class CommentInput(graphene.InputObjectType):
    """
    Input for Comments in Graphene backend.
    Type: graphene.InputObjectType
    """

    # ID field
    id=graphene.ID()

    # String fields
    text=graphene.String()

    # Input of type MeetingInput
    # Which references to the above class
    related_post=graphene.Field(MeetingInput)


class OTPInput(graphene.InputObjectType):
    """
    Input for OTP in Graphene backend.
    Type: graphene.InputObjectType
    """

    # ID field
    id=graphene.ID()

    # Int field
    otp=graphene.Int()
