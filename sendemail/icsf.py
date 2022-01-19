# Importing the libraries
from io import StringIO

import gqldemo.constants as gc

def create_ics_file(
        event_name, event_start_date, event_start_time,
        event_organizer):
    """
    This function takes event_name, event_start_date, event_start_time,
    event_organizer arguments and generate a StringIO object with contents
    of ICS file written onto it.

    :param event_name      : String, Contains the name of event
    :param event_start_date: Date, Contains the starting date of event
    :param event_start_time: Time, Contains the starting time of event
    :param event_organizer : String, Contains the email address of Organizer

    :return: StringIO object, Returns a StringIO object with ICS content written
             onto it. 
    """
    
    # Using the StringIO method to define
    # a file object.
    string_io_object=StringIO()

    # Creating a variable with Date and Time combined
    event_time=''.join(str(event_start_date).split('-')) + \
               'T' + ''.join(str(event_start_time).split(':')) + 'Z'

    # Writing ICS content to this file
    string_io_object.write("BEGIN:VCALENDAR\n")
    string_io_object.write("VERSION:2.0\n")
    string_io_object.write("PRODID:ics.py - http://git.io/lLljaA\n")
    string_io_object.write("BEGIN:VEVENT\n")
    string_io_object.write("DTSTART;TZID="+ gc.timezone +":"+str(event_time)+"\n")
    string_io_object.write("SUMMARY:"+event_name+"\n")
    string_io_object.write("UID:"+event_organizer+"\n")
    string_io_object.write("END:VEVENT\n")
    string_io_object.write("END:VCALENDAR")
    
    # Setting the file's current position to beginning
    string_io_object.seek(0)

    # returning the file object
    return string_io_object


def create_email_body(
        event_name, event_date, event_time,
        event_organizer):
    """
    This function creates a email content by taking input of event details.

    :param event_name     : String, Contains the name of event
    :param event_date     : Date, Contains the starting date of event
    :param event_time     : Time, Contains the starting time of event
    :param event_organizer: String, Contains the email address of Organizer

    :return: String, Returns a string with well structured email content
    """

    # String for salutation and other details
    text="Hi,\n\nYou are invited to \"" + event_name + "\" . Please check below details of event:\n\n"

    # String for creating event details
    event_detail="Event Name: " + event_name + "\nEvent date: " + str(event_date) + \
                   "\nEvent time: " + str(event_time) + "\
                    \nOrganized by: " + event_organizer + "\n"
    
    # Closing salutation
    ending="\n\nRegards,\nEvent Manager Admin\n\nNote: This is a computer generated email"

    # Return the combined string which will be well formated
    return(text + event_detail + ending)
