# Importing the libraries
from django.conf import settings

from django.db.models.signals import m2m_changed

from django.db.models.signals import post_save

from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from ema.models import Meeting, Users, OTP

from sendemail.tasks import send_email

from sendemail.generate_otp import getOTP

from sendemail.icsf import create_ics_file, create_email_body


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Signal when a record is inserted into database.
    model which is used in this signal is Users model which is defined
    in AUTH_USER_MODEL key in settings file.

    :param sender  : Users Model, sender is a Users model
    :param instance: Users instance, User instance
    :param created : Boolean, checks if the instance is created
    :param kwargs  : Keyword arguments
    """

    # If the record is inserted
    if created:
        # Create a token for that user instance
        Token.objects.create(user=instance)

        # Generate a six digit OTP
        otp=getOTP()

        # Creating a OTP object
        otpobj = OTP(otp=otp, owner=instance)
        # Saving the otp temporarily in db
        otpobj.save()

        # Email content with OTP and email subject
        emailMessage=otp+" is your verification OTP."
        emailSubject="Email Verification"

        # Sending the mail with the OTP
        send_email.delay(emailSubject, emailMessage, [instance.email], None)


# M2M Signal when the Meeting is completely defined
def joinee_added(sender, instance, action, *args, **kwargs):
    """
    M2M Signal when the Meeting model with Many to Many field is saved.
    Sends a email with all the details of the events to the different users
    who are attending the event.

    :param sender  : Meeting Model, sender is a Meeting model Joinee attribute
    :param instance: Meeting instance, Meeting instance
    :param created : Boolean, checks if the instance is created
    :param kwargs  : Keyword arguments
    """
    # Check if the action is 'post_add' which signifies
    # the users who are joining the events are stored in the DB
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Get the event details
        event_name=instance.title
        event_date=instance.date
        event_time=instance.time

        # Get the email ID of the organizer
        event_organizer=Users.objects.get(id=instance.owner.id).email
        
        # Get the list of Users email who are joining the event
        event_joinee=[user.email for user in instance.joinee.all()]

        # Create the attachment object with ICS file content
        attachement_object=create_ics_file(event_name, event_date,
                                           event_time, event_organizer)

        # Read the data from the StringIO object content
        data=attachement_object.read()

        # Creting the email subject for the event
        emailSubject="You are Invited to "+event_name
        
        # Create the content of the email
        emailMessage=create_email_body(event_name, event_date,
                                       event_time, event_organizer)
        
        # Send email
        send_email.delay(emailSubject, emailMessage, event_joinee, data)
        
# Defining the M2M signal with above defined function and 
# the field which gets affected trigger the signal
m2m_changed.connect(joinee_added, sender=Meeting.joinee.through)
