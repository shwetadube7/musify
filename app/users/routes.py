import logging
import sqlalchemy
from flask import Blueprint, jsonify, request

from app.users.constants import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_400_CLIENT_ERROR,
    HTTP_500_INTERNAL_SERVER_ERROR,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND,
    CLIENT_ERROR,
    CREATED,
    STATUS,
    GET,
    POST,
    PUT,
    PATCH,
    DELETE,
    LIMIT,
    OFFSET,
    MESSAGE,
    MAX_LIMIT,
    LIST_OPT_PARAMS,
    SEARCH_OPT_PARAMS
)

engine = sqlalchemy.create_engine('oracle://lab:lab@127.0.0.1:1521/xe')
connection = engine.connect()

EMPTY_SET = frozenset([])
users = Blueprint('users', __name__, url_prefix='/api/v1')
logger = logging.getLogger('app')


@users.route('/users', methods=[GET])
def list_users():
    rows = connection.execute("SELECT USER_ID, USERNAME, EMAIL_ADDR, ADDRESS, PHONE_NUM FROM USER_INFO").fetchall();
    resp = {'status': 200, 'users': []}
    for row in rows:
        user_info = {
            'user_id': row[0],
            'user_name': row[1],
            'email': row[2],
            'address': row[3],
            'phone': row[4]
        }
        resp['users'].append(user_info)

    return make_response(resp)


@users.route('/users/<user_id>', methods=[GET])
def get_users(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid user ID: {}'.format(user_id)
        }
        return make_response(resp)

    query = "SELECT USER_ID, USERNAME, EMAIL_ADDR, ADDRESS, PHONE_NUM FROM USER_INFO WHERE USER_ID = {}".format(user_id)
    row = connection.execute(query).fetchone()
    resp = {'status': 200, 'user': {}}
    user_info = {
        'user_id': row[0],
        'user_name': row[1],
        'email': row[2],
        'address': row[3],
        'phone': row[4]
    }
    resp['user'] = user_info

    return make_response(resp)


@users.route('/users/<user_id>', methods=[DELETE])
def delete_users(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid user ID: {}'.format(user_id)
        }
        return make_response(resp)

    query = "DELETE FROM USER_INFO WHERE USER_ID = {}".format(user_id)
    row = connection.execute(query)
    resp = {
        'status': 200,
        'message': 'User ID: {} deleted successfully'.format(user_id)
    }

    return make_response(resp)

@users.route('/users', methods=[POST])
def create_users():
    request_data = request.get_json(force=True)
    user_name = request_data.get("user_name")
    password = request_data.get("password", "password")
    email = request_data.get("email")
    address = request_data.get("address")
    phone = request_data.get("phone")
    request_data['password'] = password
    request_data.pop("user_id")

    transaction = connection.begin()
    resp = {}
    try:
        query = "INSERT INTO USER_INFO (USERNAME, USER_ID, USER_PASSWORD, EMAIL_ADDR, ADDRESS, PHONE_NUM) VALUES (:user_name, user_sequence.NEXTVAL, :password, :email, :address, :phone)"
        status = connection.execute(query, **request_data)
        user_seq = connection.execute('SELECT user_sequence.CURRVAL FROM DUAL').fetchone()
        transaction.commit()
        resp['status'] = 201
        resp['message'] = 'User created successfully'
        resp['user'] = {
            'user_id': user_seq[0],
            'user_name': user_name,
            'email': email,
            'address': address,
            'phone': phone
        }
    except Exception as e:
        transaction.rollback()
        logger.critical(e)
        resp['status'] = 500
        resp['message'] = 'Server Error'

    return make_response(resp)


@users.route('/users/<user_id>', methods=[PUT])
def update_users(user_id):

    request_data = request.get_json(force=True)
    user_name = request_data.get("user_name")
    password = request_data.get("password", "password")
    email = request_data.get("email")
    address = request_data.get("address")
    phone = request_data.get("phone")
    request_data['password'] = password
    request_data.pop("user_id")
    query = "UPDATE USER_INFO SET USERNAME=:user_name, USER_PASSWORD=:password, EMAIL_ADDR=:email, ADDRESS=:address, PHONE_NUM=:phone where user_id={}".format(user_id)
    logger.info("SQL Query: {}".format(query))

    resp = {}
    try:
        status = connection.execute(query, **request_data)
        resp['status'] = CREATED
        resp['message'] = 'User updated successfully'
        resp['user'] = {
            'user_id': user_id,
            'user_name': user_name,
            'email': email,
            'address': address,
            'phone': phone
        }
    except Exception as e:
        logger.critical(e)
        resp['status'] = INTERNAL_SERVER_ERROR
        resp['message'] = 'Server Error'

    return make_response(resp)
# ------------------------------------------------------------------------------
# Util Functions
# ------------------------------------------------------------------------------
def input_validator(request_data, OPT_PARAMS):
    user_params = set(request_data.keys())
    bad_params = user_params - OPT_PARAMS

    if not bad_params == EMPTY_SET:
        return True, make_response(bad_params_client_error(bad_params))

    if not int_validator(request_data.get(LIMIT, 10)):
        return True, make_response(invalid_type_client_error(LIMIT))

    if not int_validator(request_data.get(OFFSET, 10)):
        return True, make_response(invalid_type_client_error(OFFSET))

    if int(request_data.get(LIMIT, 10)) > MAX_LIMIT:
        return True, make_response(limit_exceeded_client_error())

    return False, {}


def int_validator(value):
    try:
        x = int(value)
        if x < 0:
            return False
    except ValueError:
        return False

    return True


def invalid_type_client_error(param):
    return {
        STATUS: CLIENT_ERROR,
        MESSAGE: 'Parameter [{}] must contain a positive number'.format(param)
    }


def bad_params_client_error(bad_params):
    return {
        STATUS: CLIENT_ERROR,
        MESSAGE: 'Unsuppported parameter(s) found: [{}]'.format(
            ', '.join(bad_params)
        )
    }


def limit_exceeded_client_error():
    return {
        STATUS: CLIENT_ERROR,
        MESSAGE: 'Max limit supported: {}'.format(MAX_LIMIT)
    }


def make_response(resp):
    if resp[STATUS] == INTERNAL_SERVER_ERROR: # 500
        return jsonify(resp), HTTP_500_INTERNAL_SERVER_ERROR
    elif resp[STATUS] == NOT_FOUND: # 404
        return jsonify(resp), HTTP_404_NOT_FOUND
    elif resp[STATUS] == CLIENT_ERROR: # 400
        return jsonify(resp), HTTP_400_CLIENT_ERROR
    elif resp[STATUS] == CREATED: # 201
        return jsonify(resp), HTTP_201_CREATED
    else: # 200
        return jsonify(resp), HTTP_200_OK
