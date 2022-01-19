# Registration user Mutation
registerUserMutation="""
    mutation CreateUser($email: String!, $password: String!
                        $firstName: String!, $lastName: String!) {
        createUser(input : {firstName: $firstName, lastName: $lastName,
                    email: $email, password: $password}) {
            users {
                firstName
                lastName
                email
            }
        }
    }
"""


# Password retrival query
passwordRetrival="""
    query UserByemail($email: String) {
        userByemail(email: $email) {
            password
        }
    }
"""


# Register new Event mutation
newEvent="""
    mutation NewEvent($title: String!, $date: Date!, $time: Time!,
									$description: String!, $owner:UsersInput!,
									$joinee:[UsersInput!]!) {
        createMeeting(input: {title: $title, date: $date, time: $time,
                                                    description: $description,
                                                    owner: $owner,
                                                    joinee: $joinee}) {
            meeting {
                title
                date
                time
                description
                owner {
                    email
                }
                joinee {
                    email
                }
            }
        }
    }
"""