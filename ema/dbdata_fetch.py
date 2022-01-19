# Importing the libraries
import asyncio

from django.conf import settings

import json

from python_graphql_client import GraphqlClient


# Creating a GraphQLClient with existing GraphQL backend
client=GraphqlClient(endpoint=settings.ENDPOINT, verify=False)

# Function to execute Mutation and Query in GraphQL endpoint
def executeQuery(query, variables):
    """
    This function executes query and mutations with given variable.

    :param query    : String, Contains different mutation and query
    :param variables: String, Contains value of different parameters to be used 
                      in query

    :return: JSON String, value of type JSON string returned from the Graphene backend
    """

    # Execute the query with the variables
    data=asyncio.run(client.execute_async(query=query, variables=variables))

    # Return the JSON string
    return json.dumps(data)
