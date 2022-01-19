# Importing the Libraries

# This will be used for validating the length of the text
from django.core.validators import MinLengthValidator

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models

# Create your models here.

# Create a New user and superuser
class UsersManager(BaseUserManager):
    """
    Custom usermanager defined for Custom user class. Inherits from
    BaseUserManager class
    """
    def create_user(
            self, email, password,
            first_name, last_name):
        """
        Creates the user instance by accepting different user input.

        :param email     : string, Email of the user
        :param first_name: string, First name of the user 
        :param last_name : string, Last name of the user
        :param password  : string, Password given by the user

        :return: User, returns a user instance
        """

        # If email is not provided raise Value error
        if not email:
            raise ValueError("User must have an email address")

        # Create a model for user
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        # Set user password which will be encrypted
        user.set_password(password)
        # Save the User to the db
        user.save(using=self._db)

        # return the object
        return user
    

    def create_superuser(
            self, email, password,
            first_name, last_name):
        """
        Creates the superuser instance by accepting different input.

        :param email     : string, Email of the user
        :param first_name: string, First name of the user 
        :param last_name : string, Last name of the user
        :param password  : string, Password given by the user

        :return: User, returns a user instance with additional features
                 for superuser
        """

        # Defining the attribute for superuser
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Setting Admin, staff and Superuser charateristic
        # for Superuser
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True

        # Saving the superuser to database
        user.save(using=self._db)

        # return the object
        return user


# User Model which will have the basic feature of the user Like Email ID, User name and password
class Users(AbstractBaseUser):
    """
    User Model which will have the basic feature of the user
    Like Email ID, User name and password. 

    Some other features of User model include if the user if admin,
    active, staff, superuser or verified.

    Inherits from the default Django AbstractBaseUser class.
    """

    # Email field for User with Unique attribute to true
    email=models.EmailField(null=False, unique=True)
    
    # Password, name for User with CharField
    password=models.CharField(max_length=1000, null=False)
    first_name=models.CharField(max_length=100, null=False)
    last_name=models.CharField(max_length=100, null=False)
    
    # Date Joined and Last login field with Date and Time field
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    
    # Setting Admin, Active, Staff and Superuser field 
    # with boolean field and default is set to False
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    
    # Defining a field to set True if the user is verified
    # by the OTP sent to the email. By default user is not verified
    is_checked=models.BooleanField(default=False)

    
    # Defining the Custom user manager for Users model
    objects=UsersManager()

    # Email should be used as default username field
    USERNAME_FIELD='email'

    # Password and name fields are required
    REQUIRED_FIELDS=['password', 'first_name', 'last_name',]

    def __str__(self):
        """
        Representing class object as string.

        :return: String, Email of the instance
        """
        return self.email


    def has_perm(self, perm, obj=None):
        """
        Returns if the user has specific permission

        :return: Boolean, Returns if instance is admin or not
        """
        return self.is_admin
    

    def has_module_perms(self, app_label):
        """
        Returns if the user has any permission in given package

        :return: Boolean, Always return True
        """
        return True
    

# Meeting Model
class Meeting(models.Model):
    """
    Meeting Model: This model stores all the data related to meetings, workshop, fests.
    Each event has a owner which is a user and each user can create many meeting which
    corresponds to Users class. (One-To-Many relationship)
    Each event may have one or more attendants and each user can be part of multiple meeting
    which corresponds to Users class. (Many-to-Many relationship)
    """

    # Title of the meeting with CharField and different attributes
    title=models.CharField(max_length=150, null=False)
    
    # Event date and time with Date and Time Field
    date=models.DateField(null=False)
    time=models.TimeField(null=False)
    
    # Description of the event with TextField
    description=models.TextField(validators=[MinLengthValidator(10)])

    # Foreign key and one-to-Many relationship
    owner=models.ForeignKey(Users, on_delete=models.CASCADE,
                              null=True, related_name="meetings")

    # Foreign key and many-to-may relationship with users as 
    # each event could have one or many joinee
    joinee=models.ManyToManyField(Users)

    def __str__(self):
        """
        Representing class object as string.

        :return: String, Title of the Meeting
        """
        return f"self.title"


# Comment model
class Comment(models.Model):
    """
    Comment model: Model architecture for a comment to a event
    """

    # Text field for the comment
    text=models.TextField(max_length=400) 

    # Foreign key and One-TO-Many relationship as one event could have many user
    related_post=models.ForeignKey(Meeting, on_delete=models.CASCADE,
                                     null=True, related_name="meetings")

    # Foreign key and One-To-Many relationship as multiple comment can be done by same user
    comment_owner=models.ForeignKey(Users, on_delete=models.CASCADE,
                                      null=True, related_name="users")


# OTP model
class OTP(models.Model):
    """
    OTP model: Model to store OTP created for some time
    """
    # OTP field with Integer
    otp=models.IntegerField()

    # User corresponding to the OTP
    owner=models.ForeignKey(Users, on_delete=models.CASCADE)
