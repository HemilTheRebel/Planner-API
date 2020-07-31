def delete_task_use_case(user_id, task_id, repository):
    repository.delete_task(user_id, task_id)