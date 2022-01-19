# Importing libraries
from django.contrib.auth import authenticate

import json

from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.views import APIView

from ema import userquery as uq

from ema import dbdata_fetch as ddf

from ema.models import Users, OTP

from sendemail.generate_otp import getOTP

from sendemail.tasks import send_email


# User registration View
class RegisterUser(APIView):
    """
    RegisterUser class inherited from APIView. Used to
    get all the form data from the User and save the User 
    record to the database.
    Also with new user creation it creates a token for that user.
    """
    def post(self, request):
        """
        Post method for getting the data from the User request.
        """

        # Retrieve all the values from the request
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        # Create a variable for graphene query
        register_user_variable={"email": email,
                                "firstName": first_name,
                                "lastName": last_name,
                                "password": password}

        # Execture create user query with the collected data stored in a variable
        rvalue=ddf.executeQuery(uq.registerUserMutation,
                                register_user_variable)

        # Load JSON object
        json_object=json.loads(rvalue)

        # Extracting the key from the object
        pairs=json_object.items()

        # Extracting the key value pairs and checking 
        # If "data" is in the return key
        status=False

        for key, value in pairs:
            if key == "data":
                status=True
                break

        # Creating a data dictionary
        data = {}

        # If the user data is returned
        if status:
            # Send a HTTPResponse back with Users attribute
            users=Users.objects.get(email=email)

            data['email']=users.email
            data['first_name']=users.first_name
            data['last_name']=users.last_name

            # Get the token for user and set it to token attribute
            token=Token.objects.get(user=users).key
            data['token']=token
        else:
            # If there is error then
            # set the data to None
            data=None
        return Response(data)


# Login view for the user
class LoginUser(APIView):
    """
    Login view for the User which takes Username and password; then
    logs in the user into the system and provide a token in return.
    """
    def post(self, request):
        """
        Post method for getting the data from the User request.
        """
        # Get username, password and otp
        username=request.POST.get('username')
        password=request.POST.get('password')
        otp=request.POST.get('otp')

        # Check if both entered username and password is none
        # Return appropriate error response
        if username is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        elif password is None and otp is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        
        # Authenticate Username and password
        if password is not None:
            user=authenticate(username=username, password=password)

        # If otp is provided
        elif otp is not None:
            # Check if OTP key is in session
            if 'otp' in request.session:
                # Match if otp is correct or not and the user
                # who accessed the otp is the intended user
                if(int(otp) == int(request.session['otp'])):
                    # Get the user instance 
                    user=Users.objects.get(email=username)
                    try:
                        # Delete the key from session
                        del request.session['otp']
                    except:
                        # If any error occurs 
                        # return error
                        return Response({'error': 'Something is wrong. Please try again later'},
                                        status=HTTP_404_NOT_FOUND)
                else:
                    # If user is not verified
                    # set the user instance to None
                    user=None
            else:
                # If user is not verified
                # set the user instance to None
                user=None

        # If Invalid credential
        if not user:
            return Response({'error': 'Invalid Credentials. Please check entered credentials'},
                            status=HTTP_404_NOT_FOUND)
        
        # Get the token
        token, _=Token.objects.get_or_create(user=user)
        # Return the response
        return Response({'token': token.key},
                        status=HTTP_200_OK)


class LoginWithOTP(APIView):
    """
    LoginWithOTP class to send a OTP mail to user.
    """
    def post(self, request):
        """
        Post method for getting the data from the User request.
        """
        # Get the username
        username=request.POST.get('username')

        # Generate a OTP
        otp=getOTP()

        # setting the OTP to session
        request.session['otp']=otp

        # send mail with the OTP
        subject="Login OTP"
        text=str(otp)+" is your login OTP."

        # Send mail
        send_email.delay(subject, text, [username], None)

        # Return the response
        return Response({'success':'Email sent. Please do check your email.'},
                        status=HTTP_200_OK)


# Verify User View
class VerifyUser(APIView):
    """
    Verify userview to verify the user by the OTP.
    Takes the OTP input
    """
    # Check if the user is logged in
    permission_classes=(IsAuthenticated, )

    def post(self, request):
        """
        Post method for getting the data from the User request.
        """
        # Get the data from request header
        auth_header=request.META.get("HTTP_AUTHORIZATION")

        # If autherization header is presetn
        if auth_header:
            # Get the token cleaned and retrieve user info
            # from the token
            token=auth_header.split('Token ')[1]
            user=Token.objects.get(key=token).user
        
        # Get the userinstance
        users_instance=Users.objects.get(email=user)

        # Get the otp stored and input otp
        setOTP=OTP.objects.get(owner=Users.objects.get(email=user))
        inputOTP=request.POST.get('otp')
        
        # Verify OTP
        if(int(setOTP.otp) == int(inputOTP)):
            # Set the user instance checked to true
            # and save the user instance
            # then delete the stored OTP
            users_instance.is_checked=True
            users_instance.save()
            setOTP.delete()

            # Return the response with success message
            return Response({"success": 
                            ("Thank you! You have been verified")})
        else:
            # If the verification is not processing
            # Convey user that the entered otp by user is not correct
            return Response("Please enter corrct otp")


# Logout view
class LogoutView(APIView):
    """
    LogoutView to logout the user and delete the token
    """

    # Checks if the user is logged in
    permission_classes=(IsAuthenticated,)
    
    def get(self, request):
        """
        Get method for handling this request
        """
        try:
        # deleting the session and logging out
            request.user.auth_token.delete()
        # if the keyerror happens then inform user about it
        except:
            return Response("Something is Wrong. Please try after sometime")
        # After logging out returning the response
        return Response({"success": ("Successfully logged out.")},
                        status=HTTP_200_OK)
        