import os.path
from enum import Enum, unique
from typing import List, Any, Dict

from flask import jsonify

from server.model import User, TranscriptionTask


@unique
class ResponseStatus(Enum):
    OK = 'success'
    NOK = 'failed'


class Response:
    def __init__(self) -> None:
        self.status: ResponseStatus = ResponseStatus.NOK
        self.message: str = ''
        self.exception: Exception = None
        self.errors: List[str] = None

    def to_dict(self) -> Dict[str, Any]:
        dicted = {'status': self.status.value, 'message': self.message, 'exception': None}
        if self.exception:
            dicted['exception'] = f'{self.exception}'
        if self.errors:
            dicted['errors'] = self.errors
        return dicted

    def to_flask(self, http_code: int = -1):
        if http_code == -1:
            match self.status:
                case ResponseStatus.OK:
                    http_code = 200
                case ResponseStatus.NOK:
                    http_code = 400
                case _:
                    http_code = 400
        return jsonify(self.to_dict()), http_code

    @classmethod
    def error_response(cls, message: str, exception: Exception = None, errors: List[str] = None) -> 'Response':
        response = Response()
        response.status = ResponseStatus.NOK
        response.message = message
        if exception:
            response.exception = exception
        if errors:
            response.errors = errors
        return response

    @classmethod
    def ok_response(cls, message) -> 'Response':
        response = Response()
        response.status = ResponseStatus.OK
        response.message = message
        return response


class AuthenticationResponse(Response):

    def __init__(self) -> None:
        super().__init__()
        self.token: str = ''
        self.is_authenticated: bool = False
        self.user_email: str = ''

    def to_dict(self) -> Dict[str, Any]:
        dicted = super().to_dict()
        dicted['token'] = self.token
        dicted['is_authenticated'] = self.is_authenticated
        dicted['user_email'] = self.user_email
        return dicted

    @classmethod
    def authentication_ok(cls, user: User, token: str) -> 'AuthenticationResponse':
        response = AuthenticationResponse()
        response.status = ResponseStatus.OK
        response.token = token
        response.user_email = user.email
        return response


class AudioRecordResponse(Response):

    def __init__(self) -> None:
        super().__init__()
        self.task_id: int = 0

    def to_dict(self) -> Dict[str, Any]:
        dicted = super().to_dict()
        dicted['task_id'] = self.task_id
        return dicted

    @classmethod
    def audiorecord_ok(cls, task_id: int) -> 'AudioRecordResponse':
        resp = AudioRecordResponse()
        resp.status = ResponseStatus.OK
        resp.task_id = task_id
        return resp

class ListAudioRecordResponse(Response):

    def __init__(self) -> None:
        super().__init__()
        self.records:List[Dict[str, str]] = []

    def to_dict(self) -> Dict[str, Any]:
        dicted = super().to_dict()
        dicted['records'] = self.records
        return dicted

    @classmethod
    def empty(cls):
        resp = ListAudioRecordResponse()
        resp.status = ResponseStatus.OK
        resp.records = []
        return resp

    @classmethod
    def ok(cls, records:List[TranscriptionTask]):
        resp = ListAudioRecordResponse()
        resp.status = ResponseStatus.OK
        resp.records = []
        for record in records:
            filename = os.path.basename(record.path)
            resp.records.append({
                'date': record.created_at,
                'url': f'/audio/{filename}',
                'task_id': record.id
            })
        return resp



