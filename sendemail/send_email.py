# Importing the libraries
from django.core.mail import EmailMessage

from gqldemo.settings import EMAIL_HOST_USER


def send_mail_to(
        subject, message, receiver,
        attachment=None):
    """
    This function accepts different arguments to send a email like
    subject, message, receipents, attachment for email and send the 
    email.
    This works whether there is a single receipent or multiple receipents.
    This function also add the attachment if there is any attachment given.

    :param subject   : String, Subject of the email
    :param message   : String, Content of the email
    :param receiver  : List, Contains list of email address
    :param attachment: String, Content of the email attachment. Default if the
                       attachment is not given; then accepts this parameter as
                       None

    :return: None, There is no return value from this function
    """

    # Creating a email message
    email=EmailMessage(subject, message, EMAIL_HOST_USER, receiver)

    # Check if there is any attachment
    if attachment is not None:
        # Attach the object with a .ics file extension
        email.attach('event.ics', attachment)

    # Send the email
    email.send()
