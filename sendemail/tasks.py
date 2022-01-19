# Importing the libraries
from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger

from ema.models import Meeting, Users

from gqldemo.celery import app

from sendemail.icsf import create_ics_file, create_email_body

from sendemail.send_email import send_mail_to

# Defining the Logger
logger = get_task_logger(__name__)

# Decorator of type Celery task
@app.task(name="send_email")
def send_email(
        subject, message, receiver,
        attach=None):
    """
    This function is a celery task which accepts arguments
    for email and send email with all the accepted argument.

    :param subject   : String, Subject of the email
    :param message   : String, Content of the email
    :param receiver  : List, Contains list of email address
    :param attachment: String, Content of the email attachment. Default if the
                       attachment is not given; then accepts this parameter as
                       None
    """

    # Write in the logger the message to send email
    logger.info("Email sent.")

    # Passing the values to send mail
    return send_mail_to(subject, message, receiver, attach)


# Decorator of type Celery task
@app.task(name="all_event_mail")
def all_event_mail():
    """
    This function is a celery task for sending mails for all the events
    that are present in the database. This task is specifically defined
    to use with a CRON job.
    """

    # In logger display the message of sending the email
    logger.info("Sending emails")

    # Try to send mail for all the events
    try:

        # Get all instance of meeting object one by one
        for instance in Meeting.objects.all():

            # Get and set different parameter for email sending
            event_name=instance.title
            event_date=instance.date
            event_time=instance.time

            # Getting the User email address through Users model
            event_organizer=Users.objects.get(id=instance.owner.id).email
            
            # Get all the Receipents email address from Meeting and set it in a list
            event_joinee=[user.email for user in instance.joinee.all()]

            # Create a StringIO file object by defining different custom parameters
            attachement_object=create_ics_file(event_name, event_date, event_time, event_organizer)

            # Read from the object
            data=attachement_object.read()

            # Defining the Email subject
            emailSubject="You are Invited to " + event_name
            
            # Get the content for email
            emailMessage=create_email_body(event_name, event_date, event_time, event_organizer)
            
            # Send the email
            send_email.delay(emailSubject, emailMessage, event_joinee, data)

        # After completion of task write to Logger
        logger.info("All Email sent.")

    # If any error occurs
    except:
        # Print the error message
        logger.info("Some error occured.")
