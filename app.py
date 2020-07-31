import json
from datetime import datetime, timedelta
from enum import Enum

from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity

import config
import sign_up.exceptions
import tasks.exceptions
from authenticate.repository import auth_use_case
from sign_up.repository import SignInRepository
from sign_up.use_case import sign_in_use_case
from tasks.create import create_task_use_case
from tasks.delete import delete_task_use_case
from tasks.model import Task
from tasks.repository import TaskRepository
from tasks.update import update_task_use_case


class User:
    def __init__(self, id):
        self.id = id


def authenticate(username, password):
    return User(auth_use_case(username, password))


def identity(payload):
    return User(payload['identity'])


BASE_URL = '/api/v1'

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = f'{BASE_URL}/auth'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=30)

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


class SignUpErrorCode(Enum):
    INVALID_INPUT = 0
    INVALID_EMAIL = 1
    USERNAME_ALREADY_EXISTS = 2
    EMAIL_ALREADY_EXISTS = 3


@app.route(f'{BASE_URL}/sign_up', methods=['POST'])
def sign_up_route():
    try:
        if not request.is_json:
            raise sign_up.exceptions.InvalidInput

        username = request.json.get('username', None)
        email = request.json.get('email')

        sign_in_use_case(username, email, request.json['password'], SignInRepository())

        return {
            'success': True
        }

    except (KeyError, sign_up.exceptions.InvalidInput):
        return respond_with_error(SignUpErrorCode.INVALID_INPUT)
    except sign_up.exceptions.InvalidEmail:
        return respond_with_error(SignUpErrorCode.INVALID_EMAIL)
    except sign_up.exceptions.EmailAlreadyExists:
        return respond_with_error(SignUpErrorCode.EMAIL_ALREADY_EXISTS)
    except sign_up.exceptions.UsernameAlreadyExists:
        return respond_with_error(SignUpErrorCode.USERNAME_ALREADY_EXISTS)


class CreateTaskErrorCode(Enum):
    INVALID_TASK = 0


@app.route(f'{BASE_URL}/task', methods=['POST'])
@jwt_required()
def create_task_route():
    try:
        if not request.is_json and current_identity is None:
            raise tasks.exceptions.InvalidTask

        if request.json.get('completed_before', None) is None:
            task = Task(request.json['title'],
                        request.json.get('description', None),
                        None)
        else:
            task = Task(request.json['title'],
                        request.json.get('description', None),
                        datetime.fromisoformat(request.json['completed_before'])
                        )

        return {
            'task_id': create_task_use_case(current_identity.id,
                                            task,
                                            TaskRepository())
        }

    # Value error is raised by datetime.fromisoformat when its input is not valid
    except (KeyError, tasks.exceptions.InvalidTask, ValueError):
        return respond_with_error(CreateTaskErrorCode.INVALID_TASK)


@app.route(f'{BASE_URL}/task/<task_id>', methods=['PUT'])
@jwt_required()
def update_task_route(task_id):
    try:
        if not request.is_json:
            raise tasks.exceptions.InvalidTask

        if request.json.get('complete_before', None) is None:
            task = Task(request.json['title'],
                        request.json.get('description', None),
                        None,
                        id=task_id)
        else:
            task = Task(request.json['title'],
                        request.json.get('description', None),
                        datetime.fromisoformat(request.json['complete_before']),
                        is_completed=request.json.get('is_completed', None),
                        id=task_id
                        )

        update_task_use_case(current_identity.id, task, TaskRepository())

        return {
            'success': True
        }

    # Value error is raised by datetime.fromisoformat when its input is not valid
    except (KeyError, tasks.exceptions.InvalidTask, ValueError):
        return respond_with_error(CreateTaskErrorCode.INVALID_TASK)


@app.route(f'{BASE_URL}/task/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task_route(task_id):

    delete_task_use_case(current_identity.id, task_id, TaskRepository())

    return {
        'success': True
    }


def respond_with_error(error):
    return app.response_class(
        response=json.dumps({'error': error.value}),
        status=400,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run()
