import unittest
from unittest.mock import Mock

from sign_up.exceptions import *
from sign_up.repository import SignInRepository
from sign_up.use_case import sign_in_use_case


class SignInTestCase(unittest.TestCase):
    def test_sign_in_raises_invalid_input_when_length_of_password_is_less_than_5(self):
        with self.assertRaises(InvalidInput):
            sign_in_use_case('efiutyeog', 'abc@def.com', '', Mock())

    def test_sign_in_returns_invalid_input_when_both_user_name_and_password_are_none(self):
        with self.assertRaises(InvalidInput):
            sign_in_use_case(None, None, 'eufit', Mock())

    def test_sign_in_returns_invalid_input_when_user_name_is_more_than_15(self):
        with self.assertRaises(InvalidInput):
            sign_in_use_case('1' * 17, None, 'eufit', Mock())

    def test_sign_in_returns_invalid_input_when_username_is_not_valid(self):
        with self.assertRaises(InvalidInput):
            sign_in_use_case('(*6756', None, 'eufit', Mock())

    def test_sign_in_returns_username_already_exists_when_repository_returns_true(self):
        repository = Mock(spec=SignInRepository)
        repository.user_exists.return_value = True

        with self.assertRaises(UsernameAlreadyExists):
            sign_in_use_case('6756', None, 'eufit', repository)

    def test_sign_in_raises_invalid_email_when_invalid_email(self):
        with self.assertRaises(InvalidEmail):
            sign_in_use_case(None, 'None', 'eufit', Mock())

    def test_sign_in_raises_email_exists_when_repository_returns_true(self):
        repository = Mock(spec=SignInRepository)
        repository.email_exists.return_value = True
        with self.assertRaises(EmailAlreadyExists):
            sign_in_use_case(None, 'abc@def.com', 'askfu', Mock())

    def test_success(self):
        repository = Mock(spec=SignInRepository)
        repository.email_exists.return_value = False
        repository.user_exists.return_value = False

        sign_in_use_case('dfiutf', 'abc@def.com', 'askfu', repository)

