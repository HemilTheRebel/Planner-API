from tasks.exceptions import *


def update_task_use_case(user_id, task, repository):
    if not task.is_valid() or task.id is None:
        raise InvalidTask

    return repository.update_task(user_id, task)
