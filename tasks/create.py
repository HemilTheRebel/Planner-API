from tasks.exceptions import *


def create_task_use_case(user_id, task, repository):
    if not task.is_valid():
        raise InvalidTask

    return repository.add_task(user_id, task)
