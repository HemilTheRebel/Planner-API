import psycopg2
from email_validator import validate_email, EmailNotValidError

import config
from util.input_validation import is_valid_email
from util.password import is_correct


def auth_use_case(username, password):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(config.DATABASE_URL)
        cur = conn.cursor()

        if is_valid_email(username):
            cur.execute('select id, password from Users where email = %(email)s',
                        {
                            'email': username
                        })
        else:
            cur.execute('select id, password from Users where username = %(username)s',
                        {
                            'username': username
                        })

        id, password_hash = cur.fetchone()

        if is_correct(password, password_hash):
            return id

        return None

    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

