import uuid

import psycopg2

import config


class TaskRepository:
    def add_task(self, user_id, task):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(config.DATABASE_URL)
            cur = conn.cursor()

            task_id = str(uuid.uuid4())

            cur.execute('insert into tasks(user_id, title, description, complete_before, id) '
                        'values (%s, %s, %s, %s, %s)', (user_id, task.title, task.description, task.complete_before,
                                                        task_id)
                        )

            conn.commit()

            return task_id

        finally:
            if conn is not None:
                conn.close()
            if cur is not None:
                cur.close()

    def update_task(self, user_id, task):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(config.DATABASE_URL)
            cur = conn.cursor()

            cur.execute('update tasks set '
                        'title = %(title)s, complete_before = %(comp_before)s, '
                        'description = %(desc)s, is_completed = %(is_comp)s '
                        'where id = %(id)s and user_id = %(user_id)s',
                        {
                            'title': task.title,
                            'comp_before': task.complete_before,
                            'desc': task.description,
                            'is_comp': task.is_completed,
                            'id': task.id,
                            'user_id': user_id
                        })

            conn.commit()

        finally:
            if conn is not None:
                conn.close()
            if cur is not None:
                cur.close()

    def delete_task(self, user_id, task_id):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(config.DATABASE_URL)
            cur = conn.cursor()

            cur.execute('delete from tasks where user_id = %(uid)s and id = %(t_id)s',
                        {
                            'uid': user_id,
                            't_id': task_id
                        })

            conn.commit()

        finally:
            if conn is not None:
                conn.close()
            if cur is not None:
                cur.close()
