from pymongo import MongoClient, UpdateOne, DeleteMany
from pymongo.server_api import ServerApi

def extract_username_from_email(email):
    """
    Extract the username part from the email address before the '@' symbol.

    Parameters:
    email (str): The email address.

    Returns:
    str: The username part of the email address before the '@' symbol.
    """
    try:
        return email.split('@')[0]
    except IndexError:
        return None

email = "gbogbonishe@gmail.com.com"
username = extract_username_from_email(email)
print(username)
