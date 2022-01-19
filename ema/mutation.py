# Importing the libraries
from django import db

import graphene

from ema.input import UsersInput, MeetingInput, CommentInput, OTPInput

from ema.models import Users, Meeting, Comment, OTP

from ema.type import UsersType, MeetingType, CommentType


# Create user Mutation to store user data into database
class CreateUsers(graphene.Mutation):
    """
    Create user mutation of type Graphene mutation.
    Input provided of type UsersInput. 
    After Mutation; return the Users instance
    """

    class Arguments:
        """
        Inner class for defining the input of UsersInput
        Kind.
        """
        input=UsersInput(required=True)

    # Defining the return type.
    # Return type Users Instance
    users=graphene.Field(UsersType)
    
    @staticmethod
    def mutate(root, info, input):
        """
        Mutation method for getting the user input
        and saving the user instance to database.

        :return: Users, Returns Users instance.
        """
        # Create a user instance with the input
        users_instance=Users(email=input.email,
                             first_name=input.first_name,
                             last_name=input.last_name)

        # Set password which will be encrypted at the end
        password=input.password
        users_instance.set_password(password)

        # Save the instance to DB
        users_instance.save()

        # Close the connection of DB
        db.connections.close_all()

        # Return the User instance
        return CreateUsers(users=users_instance)


class VerifyUsers(graphene.Mutation):
    """
    Verify User Mutation which will take OTP input
    and verify if the OTP is correct and verify the user.
    """
    class Arguments:
        """
        Inner class for defining input of OTPInput kind.
        """
        input=OTPInput(required=True)

    # Defining the return type of UsersType
    users=graphene.Field(UsersType)

    @staticmethod
    def mutate(root, info, input):
        """
        Mutation method for verifying the User with OTP and
        changing the verification status for User and saving
        the same into database.

        :return: Users, Returns Users instance.
        """
        # Check if Authentication token is provided or not
        if(info.context.user != "AnonymousUser"):
            # Get the user info
            user=info.context.user
            # Retrieve user object with the logged in user
            users_instance=Users.objects.get(email=user)
            # Get the OTP stored 
            setOTP=OTP.objects.get(owner=Users.objects.get(email=user))

            # Get the input OTP
            inputOTP=input.otp

            # Check if the stored and entered otp are same
            if(int(setOTP.otp) == int(inputOTP)):
                # Change the checked status to True and save the User
                users_instance.is_checked=True
                users_instance.save()

                # Delete the stored OTP
                setOTP.delete()

                # Return the user instance
                return VerifyUsers(users=users_instance)

            else:
                # If entered otp is wrong the Return None
                return VerifyUsers(users=None)

        else:
            # If authentication token not provided
            # Return User as None
            return VerifyUsers(users=None)
    

# Create New event mutation
class CreateMeeting(graphene.Mutation):
    """
    CreateMeeting class which will be used to create
    new event.
    """
    class Arguments:
        """
        Inner class for defining input of MeetingInput kind.
        """
        input=MeetingInput(required=True)

    # Generate a return type of MeetingType
    meeting=graphene.Field(MeetingType)

    @staticmethod
    def mutate(root, info, input):
        """
        Mutation method for creating a new event. 

        :return: Meeting, Returns a Meeting instance
        """

        # Check if Authentication token is provided or not
        if(info.context.user != "AnonymousUser"):

            # Create a list for Joinee
            meetjoinee=[]

            # From the user input joinee append all the User
            # To joinee list
            for joinee_input in input.joinee:
                new_joinee=Users.objects.get(email=joinee_input.email)
                meetjoinee.append(new_joinee)

            # Creating a meeting instance
            meeting_instance=Meeting(title=input.title, date=input.date,
                                    time=input.time, description=input.description,
                                    owner=Users.objects.get(email=info.context.user))
            
            # Save the user instance
            meeting_instance.save()

            # Set the many to many field and Save it
            meeting_instance.joinee.set(meetjoinee)
            meeting_instance.save()

            # Return the meeting instance
            return CreateMeeting(meeting=meeting_instance)
        else:
            # Return None if token is not provided
            return CreateMeeting(meeting=None)


# Create new comment mutatioin
class CreateComment(graphene.Mutation):
    """
    CreateComment class for creating comment when user adds
    a comment.
    """
    class Arguments:
        """
        Inner class for defining input of kind CommentInput
        """
        input=CommentInput(required=True)

    # Create Returntype of CommentType
    comment=graphene.Field(CommentType)

    @staticmethod
    def mutate(root, info, input):
        """
        Mutation method for creating a new comment. 

        :return: Comment, Returns a comment instance
        """

        # Get the meeting info from input meeting id
        meet=Meeting.objects.get(id=input.related_post.id)

        # Get the user info from the token
        user=Users.objects.get(email=info.context.user)

        # Check if the Token is provided and
        # The user who is commenting is included in the event
        # and the user if verified
        if(info.context.user != "AnonymousUser" and 
                user in meet.joinee.all() and
                user.is_checked):
            # Create the comment instance 
            comment_instance=Comment(text=input.text,
                                    related_post=meet,
                                    comment_owner=user)
            
            # Save the comment to DB
            comment_instance.save()

            # Return the comment instance
            return CreateComment(comment=comment_instance)
        else:
            # If any of the condition fails 
            # Return None
            return CreateComment(comment=None)
