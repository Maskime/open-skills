import os.path
import pathlib
from datetime import datetime, timedelta
from functools import wraps
from typing import Tuple, List

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS
from password_strength import PasswordPolicy
from pyisemail import is_email

from server.model import db, User
from server.request.request_user import RequestUserCreate, RequestUserAuthenticate
from server.mapper import converter
from server.response.base import Response, AuthenticationResponse

app = Flask(__name__)
app.config.from_object(__name__)
curr_file = pathlib.Path(os.path.abspath(__file__)).parent
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{curr_file}/openskills.db'
app.config['SECRET_KEY'] = 'secretkeyofthedeaththatkillsyou'

CORS(app, resources={r'/*': {'origins': '*'}})

db.init_app(app)


def validate_request_usercreate(user_request: RequestUserCreate) -> Tuple[bool, List[str]]:
    errors = []
    email_is_valid = is_email(user_request.email)
    if not email_is_valid:
        errors.append('e-mail is invalid')
    policy = PasswordPolicy.from_names(length=8)
    pwd_errors = policy.test(user_request.password)
    if len(pwd_errors):
        errors.append('Password is not strong enough')
    return len(errors) == 0, errors


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        if len(auth_headers) != 2:
            return Response.error_response('Invalid authentication headers').to_flask(401)
        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                return Response.error_response('Invalid authentication').to_flask(401)
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return Response.error_response('Expired session').to_flask(401)
        except (jwt.InvalidTokenError, Exception) as e:
            return Response.error_response('Invalid authentication token', exception=e).to_flask(401)

    return _verify


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


@app.route('/users/authenticate', methods=['POST'])
def user_authenticate():
    user_request: RequestUserAuthenticate = converter.convert(request.get_json(), RequestUserAuthenticate)
    user_db = User.authenticate(user_request.email, user_request.password)
    if not user_db:
        return Response.error_response('Invalid credentials').to_flask()
    token = jwt.encode({
        'sub': user_db.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET_KEY'])
    return AuthenticationResponse.authentication_ok(user_db, token).to_flask()

@app.route('/experiences/create', methods=['POST'])
@token_required
def experience_create():
    pass


if __name__ == '__main__':
    app.run()
