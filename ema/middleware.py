# Importing the library
from rest_framework.authtoken.models import Token

class DRFAuthorizationMiddleware(object):
    """
    This piece of middleware adds the DRF user to each graphql resolver's context
    """
    def __init__(self):
        pass


    def resolve(self, next, root, info, **args):
        """
        Function to retrieve the token passed in the header
        and identifies the user from the token and set the
        user to info context

        :param next: represents the execution chain
        :param root: is the root value object passed throughout the query
        :param info: resolver info
        :param args: dict of arguments passed to the field
        """

        # Get the Header from the URL
        auth_header=info.context.META.get("HTTP_AUTHORIZATION")

        # Check If header is present
        if auth_header:
            # Filter the token out of the header
            token=auth_header.split('Token ')[1]

            # Get the User object from the token
            user=Token.objects.get(key=token).user

            # Set that User to context
            info.context.user=user
            
        return next(root, info, **args)
