# Importing the libraries
from django import forms

from wtforms.validators import EqualTo

class UsersForm(forms.Form):
    """
    This class is defined with different parameters 
    of user form.
    """

    # Defining the User name fields with custom error message
    first_name=forms.CharField(label="First Name", min_length = 1, max_length=100,
                                 error_messages={
                                    "required":"First name must not be empty!",
                                    "max_length": "Please enter a shorter name!"
                                })

    last_name=forms.CharField(label="Last Name", min_length=1, max_length=100, 
                                error_messages={
                                    "required":"Last name must not be empty!",
                                    "max_length": "Please enter a shorter name!"
                                })
                                
    # Defining the email address field with condition and error messages                            
    email_address=forms.EmailField(label="Email Address", error_messages= {
        "required": "Please fill this Field"
    })

    # Password field with Min and Max length with required field
    password=forms.CharField(label="Password", min_length=8, max_length=32, error_messages={
        "required": "Please fill out this field",
        "max_length": "The entered password is too long",
        "min_length": "The entered password is too short"
    })

    # Password field with validator to check if previously entered password is matching or not
    retypepassword=forms.CharField(label="Retype Password", min_length=8, max_length=32,
                                    validators=[EqualTo('password')])
