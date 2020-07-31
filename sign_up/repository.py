import uuid

import psycopg2

import config


class SignInRepository:
    def user_exists(self, username):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(config.DATABASE_URL)
            cur = conn.cursor()

            cur.execute('select id from users where username = %(username)s',
                        {
                            'username': username
                        })

            cur.fetchone()

            # id is primary key. So rowcount will always be either 1 or 0. If it is 0, user does not exist else they do
            return cur.rowcount == 1

        finally:
            if conn is not None:
                conn.close()
            if cur is not None:
                cur.close()

    def email_exists(self, email):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(config.DATABASE_URL)
            cur = conn.cursor()

            cur.execute('select id from users where email = %(email)s',
                        {
                            'email': email
                        })

            cur.fetchone()

            # id is primary key. So rowcount will always be either 1 or 0. If it is 0, user does not exist else they do
            return cur.rowcount == 1

        finally:
            if conn is not None:
                conn.close()
            if cur is not None:
                cur.close()

    def add(self, username, email, password):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(config.DATABASE_URL)
            cur = conn.cursor()

            user_id = str(uuid.uuid4())

            if username is not None and email is not None:
                cur.execute('insert into users (id, username, email, password) values (%s, %s, %s, %s)',
                            (user_id, username, email, password))
            if username is not None and email is None:
                cur.execute('insert into users (id, username, password) values (%s, %s, %s)',
                            (user_id, username, password))
            if email is not None and username is None:
                cur.execute('insert into users (id, email, password) values (%s, %s, %s)',
                            (user_id, email, password))

            conn.commit()

        finally:
            if conn is not None:
                conn.close()
            if cur is not None:
                cur.close()
