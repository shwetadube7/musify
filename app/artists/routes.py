import logging
import sqlalchemy
from flask import Blueprint, jsonify, request

from app.artists.constants import (
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
artists = Blueprint('artists', __name__, url_prefix='/api/v1')
logger = logging.getLogger('app')


@artists.route('/artists', methods=[GET])
def list_artists():
    rows = connection.execute("SELECT ARTIST_NAME, ARTIST_ID FROM ARTIST").fetchall();
    resp = {'status': 200, 'artists': []}
    for row in rows:
        artist_info = {
            'artist_name': row[0],
            'artist_id': row[1]
        }
        resp['artists'].append(artist_info)

    return make_response(resp)


@artists.route('/artists/<artist_id>', methods=[GET])
def get_artists(artist_id):
    try:
        artist_id = int(artist_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid artist ID: {}'.format(artist_id)
        }
        return make_response(resp)

    query = "SELECT ARTIST_NAME FROM ARTIST WHERE ARTIST_ID = {}".format(artist_id)
    row = connection.execute(query).fetchone()
    resp = {'status': 200, 'artist': {}}
    artist_info = {
        'artist_name': row[0],
    }
    resp['artist'] = artist_info

    return make_response(resp)


@artists.route('/artists/<artist_id>', methods=[DELETE])
def delete_artists(artist_id):
    try:
        artist_id = int(artist_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid artist ID: {}'.format(artist_id)
        }
        return make_response(resp)

    query = "DELETE FROM ARTIST WHERE ARTIST_ID = {}".format(artist_id)
    row = connection.execute(query)
    resp = {
        'status': 200,
        'message': 'Artist ID: {} deleted successfully'.format(artist_id)
    }

    return make_response(resp)

@artists.route('/artists', methods=[POST])
def create_artists():
    request_data = request.get_json(force=True)
    artist_name = request_data.get("artist_name")
    request_data.pop("artist_id")

    query = "INSERT INTO ARTIST (ARTIST_NAME, ARTIST_ID) VALUES (:artist_name, artist_sequence.NEXTVAL)"

    resp = {}
    try:
        status = connection.execute(query, **request_data)
        resp['status'] = 201
        resp['message'] = 'Artist created successfully'
        resp['artist'] = {
            'artist_name': artist_name,
        }
    except Exception as e:
        logger.critical(e)
        resp['status'] = 500
        resp['message'] = 'Server Error'

    return make_response(resp)


@artists.route('/artists/<artist_id>', methods=[PUT])
def update_artists(artist_id):

    request_data = request.get_json(force=True)
    artist_name = request_data.get("artist_name")
    request_data.pop("artist_id")
    query = "UPDATE ARTIST SET ARTIST_NAME=:artist_name where artist_id={}".format(artist_id)
    logger.info("SQL Query: {}".format(query))

    resp = {}
    try:
        status = connection.execute(query, **request_data)
        resp['status'] = CREATED
        resp['message'] = 'Artist updated successfully'
        resp['artist'] = {
            'artist_id': artist_id,
            'artist_name': artist_name,
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
    artist_params = set(request_data.keys())
    bad_params = artist_params - OPT_PARAMS

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
