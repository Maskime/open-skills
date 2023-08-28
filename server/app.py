import os.path
import pathlib
from typing import Tuple, List

from flask import Flask, jsonify, request
from flask_cors import CORS
from password_strength import PasswordPolicy
from pyisemail import is_email

from server.model import db, User
from server.request.request_user import RequestUserCreate
from server.mapper import converter
from server.response.base import Response

app = Flask(__name__)
app.config.from_object(__name__)
curr_file = pathlib.Path(os.path.abspath(__file__)).parent
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{curr_file}/openskills.db'

CORS(app, resources={r'/*': {'origins': '*'}})

db.init_app(app)


def validate_request_usercreate(user_request: RequestUserCreate) -> Tuple[bool, List[str]]:
    errors = []
    email_is_valid = is_email(user_request.email, check_dns=True)
    if not email_is_valid:
        errors.append('e-mail is invalid')
    policy = PasswordPolicy.from_names(length=8, uppercase=1, numbers=1, special=1)
    pwd_errors = policy.test(user_request.password)
    if len(pwd_errors):
        errors.append('Password is not strong enough')
    return len(errors) == 0, errors


@app.route('/users/register', methods=['POST'])
def user_register():
    if request.method != 'POST':
        return Response.error_response('Unexpected http verb').to_flask()
    try:
        user_request = converter.convert(request.get_json(), RequestUserCreate)
        is_valid, errors = validate_request_usercreate(user_request)
        if not is_valid:
            return Response.error_response('Error occurred while validating request:', errors=errors).to_flask()
        user_db = User.query.filter_by(email=user_request.email).first()
        if user_db:
            return Response.error_response('A user with this e-mail already exists').to_flask()
        user_db = converter.convert(user_request, User)
        db.session.add(user_db)
        db.session.commit()
        return Response.ok_response('User created').to_flask()
    except Exception as e:
        return Response.error_response('An error occurred', e).to_flask(500)


if __name__ == '__main__':
    app.run()
