# Importing the libraries
import math
import random

def getOTP():
    """
    getOTP() generates unique 6 digit otp.

    :return: string,returns a 6 digit string otp
    """
    # Digits from 0 to 9
    digits="0123456789"

    # Creating a OTP variable
    OTP=""

    # Create the OTP
    for _ in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    
    # return the OTP 
    return OTP
