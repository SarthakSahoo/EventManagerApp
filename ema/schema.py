# Importing the libraries
import graphene

from graphene_django.filter import DjangoFilterConnectionField

from ema.filter import MeetingNode

from ema.input import MeetingInput

from ema.models import Users, Meeting, Comment

from ema.mutation import CreateUsers, CreateMeeting, CreateComment, VerifyUsers

from ema.query import Query

from ema.type import UsersType, MeetingType, CommentType


class Mutation(graphene.ObjectType):
    """
    Mutation class for defining all the mutations
    together.
    Mutation class of type Graphene Object type
    """
    create_user=CreateUsers.Field()
    create_meeting=CreateMeeting.Field()
    create_comment=CreateComment.Field()
    verify_users=VerifyUsers.Field()


class Query(graphene.ObjectType):
    """
    Query class for querying different things from graphene
    backend with different parameters.
    Query class of type Graphene object type.
    """

    # Get all the data of different models
    all_users=graphene.List(UsersType)
    all_meetings=graphene.List(MeetingType)
    all_comments=graphene.List(CommentType)

    # Defining the Filter nodes
    event=graphene.relay.Node.Field(MeetingNode)
    all_event=DjangoFilterConnectionField(MeetingNode, date=graphene.Date())

    # Field for accessing data based on certain condidtions
    user_by_email=graphene.Field(UsersType, email=graphene.String())

    meeting_by_email=graphene.Field(MeetingType, email=graphene.String())
    meeting_by_joinee=graphene.List(MeetingType, email=graphene.String())
    meeting_details_by_id=graphene.Field(MeetingType, id=graphene.ID())
    meeting_by_date=graphene.Field(MeetingType, date=graphene.Date())

    comment_by_meeting=graphene.List(CommentType, id=graphene.ID())

    # Resolver function for accessing all User Info
    def resolve_all_users(root, info):
        """
        Resolver function for Getting all the user information.

        :return: QuerySet, returns a query set of Users instances
        """
        return Users.objects.all()
    

    # Resolver function for accessing all even info
    def resolve_all_meetings(root, info):
        """
        Resolver function for Getting all the Meeting information.

        :return: QuerySet, returns a query set of Meeting instances
        """

        # Check if the header has the token else return None
        if info.context.user != "AnonymousUser":
            return Meeting.objects.all()
        else:
            return None


    # Resolver function for accessing all comment
    def resolve_all_comments(root, info):
        """
        Resolver function for Getting all the Comment information.

        :return: QuerySet, returns a query set of Comment instances
        """

        # Check if the header has the token else return None
        if info.context.user != "AnonymousUser":
            return Comment.objects.all()
        else:
            return None


    # Resolver function for accessing user by particular email address
    def resolve_user_by_email(root, info, email):
        """
        Resolver function for returning a User instance based on the 
        input email address.

        :return: Users, returns a Users instance
        """
        try:
            # Check if the header has the token else return None
            if info.context.user != "AnonymousUser":
                user=Users.objects.get(email=email)
            else:
                return None
        # If the user is not in the database
        except Users.DoesNotExist:
            user=None
        return user


    # Resolver function for accessing meeting by the email address of the owner
    def resolve_meeting_by_email(root, info, email):
        """
        Resolver function for returning a meeting instance based on the 
        owner email address

        :return: Meeting, returns a Meeting instance
        """
        try:
            # Check if the header has the token else return None
            if info.context.user != "AnonymousUser":
                meet=Meeting.objects.get(
                    owner=Users.objects.get(email=email)
                )
            else:
                return None
        # If the Meeting instance is not in database
        except Meeting.DoesNotExist:
            meet=None
        return meet


    # Resolver function for accessing joinee in the meeting email address
    def resolve_meeting_by_joinee(root, info, email):
        """
        Resolver funtion for returning a meeting instance based on the 
        Joinee email address

        :return: Meeting, returns a Meeting instance
        """
        try:
            # Check if the header has the token else return None
            if info.context.user != "AnonymousUser":
                meet= Meeting.objects.filter(
                    joinee=Users.objects.get(email=email)
                )
            else:
                return None
        # If the meeting instance is not in database
        except Meeting.DoesNotExist:
            meet=None
        return meet


    # Resolver function for accessing meeting details by meeting ID
    def resolve_meeting_details_by_id(root, info, id):
        """
        Resolver function for returning a Meeting instance based on the
        meeting ID.

        :return: Meeting, returns a Meeting instance
        """
        try:
            # Check if the header has the token else return None
            if info.context.user != "AnonymousUser":
                event=Meeting.objects.get(id=id)
            else:
                return None
        # If the meeting instance is not in database
        except:
            event = None
        return event


    # Resolver function for accessing meeting details which are greater than current date
    def resolve_meeting_by_date(root, info, date):
        """
        Resolver function for returing meeting instance based on 
        Filter condiiton

        :return: Meeting, returns a Meeting Instance
        """
        event=Meeting.objects.get(MeetingInput.date__gt(date))
        return event


    # Resolver function for accessing comment by each event type
    def resolve_comment_by_meeting(root, info, id):
        """
        Resolver function for accessing Comment instance based on
        ID.

        :return: Comment, returns a Comment instance
        """
        try:
            if info.context.user != "AnonymousUser":
                comment=Comment.objects.filter(
                    related_post=Meeting.objects.get(id=id)
                )
            else:
                return None
        # If the comment instance is not present
        except:
            comment=None
        return comment


# Defining the schema with Query and Mutation
schema=graphene.Schema(query=Query, mutation=Mutation)
