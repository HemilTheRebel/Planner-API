import re

from email_validator import validate_email, EmailNotValidError


def is_valid_email(username):
    try:
        validate_email(username).email
    except EmailNotValidError as error:
        return False

    return True


def is_alphanumeric_underscore_or_space(string):
    return re.search(r'^[\w\s]+$', string) is not None
