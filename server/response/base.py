from enum import Enum, unique
from typing import List

from flask import jsonify


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

    def to_dict(self):
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
