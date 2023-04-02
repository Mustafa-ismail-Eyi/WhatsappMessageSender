from database_templates import User, Contacts, Messages, ContactsType, MessageType


user = User(
    user_password = "12345",
    user_phone = "+905445056671"
)

contacts = [
    Contacts(
    contact_name = "grup1",
    contact_surname = "",
    contact_phone = "LVlngjI61ef5pIMhTSmIf6",
    contact_type = ContactsType.group
    ),
    Contacts(
    contact_name = "annem",
    contact_surname = "annem1",
    contact_phone = "+905511886413",
    contact_type = ContactsType.person
    ),
]


messages = [ 
    Messages(
    message_body = "Hello World!",
    message_type = MessageType.daily,
    )
]
