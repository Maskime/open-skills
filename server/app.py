import json
import os.path
import pathlib
import shutil
from collections import namedtuple
from datetime import datetime, timedelta
from functools import wraps
from typing import Tuple, List, Callable, Dict, Optional

import filetype
import flask
import jwt
import openai
from flask import Flask, request, Request, send_from_directory
from flask_cors import CORS
from flask_socketio import send, SocketIO, emit
from password_strength import PasswordPolicy
from pyisemail import is_email

from response.base import Response, AuthenticationResponse, AudioRecordResponse, ListAudioRecordResponse
from server.mapper import converter
from server.model import db, User, TranscriptionTask
from server.request.request_user import RequestUserCreate, RequestUserAuthenticate

app = Flask(__name__)
app.config.from_object(__name__)
curr_file = pathlib.Path(os.path.abspath(__file__)).parent
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{curr_file}/openskills.db'
app.config['SECRET_KEY'] = 'secretkeyofthedeaththatkillsyou'
app.config['UPLOAD_DIR'] = '/home/maxoumask/Documents/dev/flask-vue-crud/server/uploads'
socketio = SocketIO(app, cors_allowed_origins="*")
openai.api_key = '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'

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


def validate_token(token: str) -> User:
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
    user = User.query.filter_by(email=data['sub']).first()
    if not user:
        raise ValueError('Invalid token')
    return user


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = []
        if 'Authorization' in request.headers:
            auth_headers = request.headers.get('Authorization', '').split()
        elif 'token' in request.args:
            auth_headers = ['Bearer', request.args.get('token', '')]
        if len(auth_headers) != 2:
            return Response.error_response('Invalid authentication headers').to_flask(401)
        try:
            user = validate_token(auth_headers[1])
            return f(user, *args, **kwargs)
        except ValueError:
            return Response.error_response('Invalid token').to_flask(401)
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
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return AuthenticationResponse.authentication_ok(user_db, token).to_flask()


@app.route('/audio/<filename>')
@token_required
def audio_records(user: User, filename: str):
    full_path = pathlib.Path(os.path.join(app.config['UPLOAD_DIR'], filename))
    if not full_path.is_file():
        return Response.error_response('Nope').to_flask(400)
    associated_task: TranscriptionTask = TranscriptionTask.query.filter_by(path=str(full_path)).first()
    if not associated_task:
        return Response.error_response('Nope').to_flask(400)
    if associated_task.user_id != user.id:
        return Response.error_response('Nope').to_flask(400)
    return send_from_directory(app.config['UPLOAD_DIR'], filename)


def handle_upload(user: User, req: Request):
    if 'file' not in req.files:
        return Response.error_response('No file part in the request').to_flask()
    file = req.files['file']
    utcnow = datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S")
    file_path = os.path.join(app.config['UPLOAD_DIR'], f'{user.id}_{utcnow}')
    file.save(file_path)
    kind = filetype.guess(file_path)
    if kind is None:
        os.remove(file_path)
        return Response.error_response('Could not find file type').to_flask()
    if kind.extension != 'wav':
        return Response.error_response('Invalid file type').to_flask()
    final_path = f'{file_path}.wav'
    shutil.move(file_path, final_path)
    transcription = TranscriptionTask()
    transcription.path = final_path
    transcription.status = 'not_started'
    transcription.user_id = user.id
    transcription.created_at = datetime.utcnow()
    db.session.add(transcription)
    db.session.flush()
    db.session.commit()
    return AudioRecordResponse.audiorecord_ok(transcription.id).to_flask()


def get_records_list(user: User):
    records: List[TranscriptionTask] = (TranscriptionTask
                                        .query
                                        .filter_by(user_id=user.id)
                                        .order_by(TranscriptionTask.created_at.desc())
                                        .limit(1)
                                        .all())
    if not records:
        return ListAudioRecordResponse.empty().to_flask()
    if len(records) > 0:
        return ListAudioRecordResponse.ok(records).to_flask()
    return ListAudioRecordResponse.empty().to_flask()


@app.route('/experiences/audiorecord', methods=['POST', 'GET'])
@token_required
def experience_audiorecord(user: User):
    if request.method == 'POST':
        return handle_upload(user, request)
    if request.method == 'GET':
        return get_records_list(user)


def user_task(data) -> Tuple[Optional[User], Optional[TranscriptionTask]]:
    user = validate_token(data['token'])
    task_id = data['task_id']
    task: TranscriptionTask = TranscriptionTask.query.filter_by(id=task_id).first()
    if task is None or task.user_id != user.id:
        emit('invalid_taskid', {"task_id": task_id})
        return user, None
    return user, task


@socketio.on('audio_transcription')
def audiotransciption_status(data):
    try:
        user, task = user_task(data)
        emit_task_status('Demande de transcription à Whisper-OpenAI')
        with open(task.path, 'rb') as audio_file:
            transcription = openai.Audio.transcribe('whisper-1', audio_file)
            if transcription:
                emit('transcription_received', transcription, json=True)
                TranscriptionTask.update_status(task, 'sent')
            else:
                emit('transcription_error',
                     {'message': 'Une erreur est survenue lors de la transcription du fichier audio'}, json=True)
    except ValueError:
        send('invalid_token')


prompt_tpl = """
Le texte qui va suivre est le descriptif de mission d'un consultant en informatique:
###TRANSCRIPTION###
Le but est de produire un curriculum vitae, formalise tes reponses en consequences.
"""

FunctionDescription = namedtuple("FunctionDescription", ["name", "description", "required_parameters"])


def emit_task_status(status):
    emit('task_status', {'status': status}, json=True)


def validate_response(result):
    if "choices" not in result:
        return {}
    if not len(result["choices"]):
        return {}
    if "message" not in result["choices"][0]:
        return {}
    if "function_call" not in result["choices"][0]["message"]:
        return {}
    if "arguments" not in result["choices"][0]["message"]["function_call"]:
        return {}
    try:
        args = json.loads(result["choices"][0]["message"]["function_call"]["arguments"])
        return args
    except Exception as e:
        print(f'An error occurred when loading json {e}')
        return {}


def chat_completion_params(transcription, func_desc: FunctionDescription, properties):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                'role': 'system',
                'content': 'Tu es un expert en création de CV, les réponses que tu donnes doivent concises et vont être utilisée dans un CV.'
            },
            {
                'role': 'user',
                'content': prompt_tpl.replace("###TRANSCRIPTION###", transcription),
            }
        ],
        functions=[{
            "name": func_desc.name,
            "description": func_desc.description,
            "parameters": {
                "type": "object",
                "properties": properties
            },
            "required": func_desc.required_parameters
        }]
    )
    return validate_response(result)


ExpHeader = namedtuple("ExpHeader", ["company_name", "start_date", "end_date", "is_current_position", "position_name"])


def add_default_values(default_values, args):
    for default_value in default_values:
        if default_value not in args:
            args[default_value] = default_values[default_value]
    return args


def extract_exp_header(transcription) -> ExpHeader:
    emit_task_status("Extraction de l'entête")
    parameters = {
        "company_name": {
            "type": "string",
            "description": "Nom de l'entreprise dans laquelle le consultant a fait la mission decrite dans le descriptif"
        },
        "position_name": {
            "type": "string",
            "description": "Nom du poste occupé par le consultant pendant la mission",
        },
        "start_date": {
            "type": "string",
            "description": "Date de debut de la mission du consultant, exprimee au format MM/AAAA"
        },
        "end_date": {
            "type": "string",
            "description": "Date de fin de la mission du consultant, exprimee au format MM/AA"
        },
        "is_current_position": {
            "type": "boolean",
            "description": "Indique si le descriptif de mission est celui de la mission actuelle du consultant, true si c'est la mission actuelle, false si ce n'est pas la mission actuelle"
        }
    }
    func_desc = FunctionDescription("get_exp_header",
                                    "Utilise les infos de bases d'un descriptif de mission pour la generation de CV",
                                    ["company_name", "start_date"])
    args = chat_completion_params(transcription, func_desc, parameters)
    default_values = {
        'company_name': '',
        'start_date': '',
        'end_date': '',
        'is_current_position': False,
        'position_name': ''
    }
    args = add_default_values(default_values, args)
    return ExpHeader(args["company_name"], args["start_date"], args["end_date"], args["is_current_position"],
                     args["position_name"])


CompanyDetails = namedtuple("CompanyDetails", ["name", "activities"])


def extract_company_details(transcription) -> CompanyDetails:
    emit_task_status("Extraction des informations de l'entreprise")
    func_desc = FunctionDescription("get_company_details",
                                    "Recupere les informations d'une entreprise dans le descriptif de mission",
                                    ['company_name', 'company_activities'])
    properties = {
        "company_name": {
            "type": "string",
            "description": "Nom de l'entreprise dans laquelle le consultant a effectue la mission"
        },
        "company_activities": {
            "type": "string",
            "description": "Description des activites de l'entreprise"
        }
    }
    args = chat_completion_params(transcription, func_desc, properties)
    default_values = {
        'company_name': '',
        'company_activities': ''
    }
    args = add_default_values(default_values, args)
    return CompanyDetails(args["company_name"], args["company_activities"])


ProjectDetails = namedtuple("ProjectDetails", ["name", "description", "task_list"])


def extract_project_details(transcription):
    emit_task_status("Extraction des informations du projet")
    func_desc = FunctionDescription('get_project_details',
                                    "Recupere les informations concernant le projet dans le descriptif de mission du consultant",
                                    ['project_name', 'project_description'])
    properties = {
        "project_name": {
            "type": "string",
            "description": "Nom du projet sur lequel le consultant a travaille pendant sa mission"
        },
        "project_description": {
            "type": "string",
            "description": "Description du projet sur lequel le consultant a travaille"
        },
        "project_tasks": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "La liste des tâches effectuées par le consultants pendant la mission."
        }
    }
    args = chat_completion_params(transcription, func_desc, properties)
    default_values = {
        'project_name': '',
        'project_description': '',
        'project_tasks': ''
    }
    args = add_default_values(default_values, args)
    return ProjectDetails(args['project_name'], args['project_description'], args['project_tasks'])


TeamDetails = namedtuple("TeamDetails", ["size", "composition"])


def extract_team_details(transcription):
    emit_task_status("Extraction du détail de l'équipe")
    func_desc = FunctionDescription(
        'get_team_details',
        "Recupere le detail de la composition de l'equipe dans laquelle le consultant a effectue la mission",
        ["team_size", "team_composition"])
    properties = {
        "team_size": {
            "type": "string",
            "description": "Taille de l'equipe dans laquelle le consultant a effectue la mission"
        },
        "team_composition": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Liste les differentes informations a propos de la composition de l'equipe avec laquelle le consultant a travaille pendant la mission"
        }
    }
    args = chat_completion_params(transcription, func_desc, properties)
    default_values = {
        'team_size': 0,
        'team_composition': []
    }
    args = add_default_values(default_values, args)
    return TeamDetails(args["team_size"], args["team_composition"])


def extract_tech_details(transcription):
    emit_task_status("Extraction de la liste des technologies")
    func_desc = FunctionDescription(
        "get_techs_list",
        "Recupere la liste des technologies utilisee pendant la mission du consultant",
        ["tech_list"])
    properties = {
        "tech_list": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "La liste des technologies utilisees par le consultant lors de la mission"
        }
    }
    args = chat_completion_params(transcription, func_desc, properties)
    if "tech_list" not in args:
        return []
    return args["tech_list"]


@socketio.on('start_extraction')
def start_extraction(data):
    try:
        user, task = user_task(data)
        transcription = data['transcription']
        header = extract_exp_header(transcription)
        comp_details = extract_company_details(transcription)
        project_details = extract_project_details(transcription)
        team_details = extract_team_details(transcription)
        tech_details = extract_tech_details(transcription)
        result = {
            'header': header._asdict(),
            'comp_details': comp_details._asdict(),
            'project_details': project_details._asdict(),
            'team_details': team_details._asdict(),
            'tech_details': tech_details
        }
        emit('extraction_result', result, json=True)
    except Exception as e:
        emit('server_error', {'error': e}, json=True)


if __name__ == '__main__':
    socketio.run(app)
