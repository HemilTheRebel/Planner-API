from email_validator import validate_email, EmailNotValidError

from sign_up.exceptions import *
from util.input_validation import is_alphanumeric_underscore_or_space, is_valid_email
from util.password import hash_password


def sign_in_use_case(username, email, password, repository):

    if len(password) < 5:
        raise InvalidInput

    if username is not None:
        if len(username) > 15:
            raise InvalidInput

        if not is_alphanumeric_underscore_or_space(username):
            raise InvalidInput

        if repository.user_exists(username):
            raise UsernameAlreadyExists

    elif email is not None:
        if not is_valid_email(email):
            raise InvalidEmail

        if repository.email_exists(email):
            raise EmailAlreadyExists

    else:
        raise InvalidInput

    password = hash_password(password)

    repository.add(username, email, password)
