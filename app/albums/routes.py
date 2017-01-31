import logging
import sqlalchemy
from flask import Blueprint, jsonify, request

from app.albums.constants import (
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
albums = Blueprint('albums', __name__, url_prefix='/api/v1')
logger = logging.getLogger('app')


@albums.route('/albums', methods=[GET])
def list_albums():
    rows = connection.execute("SELECT A.ALBUM_NAME, B.ARTIST_NAME, A.ALBUM_ID FROM ALBUM A JOIN ARTIST B USING (ARTIST_ID)").fetchall();
    resp = {'status': HTTP_200_OK, 'albums': []}
    for row in rows:
        album_info = {
            'album_name': row[0],
            'artist_name': row[1],
            'album_id': row[2]
        }
        resp['albums'].append(album_info)

    return make_response(resp)


@albums.route('/albums/<album_id>', methods=[GET])
def get_albums(album_id):
    try:
        album_id = int(album_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid album ID: {}'.format(album_id)
        }
        return make_response(resp)

    query = "SELECT A.ALBUM_NAME, B.ARTIST_NAME FROM ALBUM A JOIN ARTIST B USING(ARTIST_ID) WHERE A.ALBUM_ID = {}".format(album_id)
    row = connection.execute(query).fetchone()
    resp = {'status': 200, 'album': {}}
    album_info = {
        'album_id': album_id,
        'album_name': row[0],
        'artist_name': row[1]
    }
    resp['album'] = album_info

    return make_response(resp)


@albums.route('/albums/<album_id>/tracks', methods=[GET])
def get_tracks(album_id):
    try:
        album_id = int(album_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid album ID: {}'.format(album_id)
        }
        return make_response(resp)

    query = "SELECT T.TRACK_ID, T.TRACK_NAME, A.ARTIST_NAME, G.GENRE_DESC FROM TRACK T FULL OUTER JOIN ARTIST A ON T.ARTIST_ID = A.ARTIST_ID FULL OUTER JOIN GENRE G ON T.ARTIST_ID = G.ARTIST_ID WHERE T.ALBUM_ID = {}".format(album_id)
    rows = connection.execute(query).fetchall()
    resp = {'status': 200, 'tracks': []}
    for row in rows:
        track_info = {
            'track_id': row[0],
            'track_name': row[1],
            'artist_name': row[2],
            'genre': row[3],
            'album_name': album_id
        }
        resp['tracks'].append(track_info)

    return make_response(resp)


@albums.route('/albums/<album_id>', methods=[DELETE])
def delete_albums(album_id):
    try:
        album_id = int(album_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid album ID: {}'.format(album_id)
        }
        return make_response(resp)
    query = "DELETE FROM GENRE WHERE ALBUM_ID = {}".format(album_id)
    query = "DELETE FROM ALBUM WHERE ALBUM_ID = {}".format(album_id)
    row = connection.execute(query)
    resp = {
        'status': 200,
        'message': 'Album ID: {} deleted successfully'.format(album_id)
    }

    return make_response(resp)

@albums.route('/albums', methods=[POST])
def create_albums():
    request_data = request.get_json(force=True)
    album_name = request_data.get("album_name")
    artist_name = request_data.get("artist_name")
    request_data.pop("album_id")
    artist = connection.execute("select artist_id from artist where artist_name=:artist_name", **{'artist_name': artist_name}).fetchone()
    resp = {}
    transaction = connection.begin()
    try:
        if artist is None:
            insert = "INSERT INTO ARTIST(ARTIST_ID, ARTIST_NAME) values(artist_sequence.NEXTVAL, :artist_name)"
            row = connection.execute(insert, **{'artist_name': artist_name})
            query = "INSERT INTO ALBUM (ALBUM_NAME, ALBUM_ID, ARTIST_ID) VALUES (:album_name, album_sequence.NEXTVAL, artist_sequence.CURRVAL)"
            row = connection.execute(query, **{'album_name': request_data.get('album_name')})
        else:
            query = "INSERT INTO ALBUM (ALBUM_NAME, ALBUM_ID, ARTIST_ID) VALUES (:album_name, album_sequence.NEXTVAL, :artist_id)"
            row = connection.execute(query, **{'album_name': album_name, 'artist_id': artist[0]})

        album_seq = connection.execute('SELECT album_sequence.CURRVAL FROM DUAL').fetchone()

        transaction.commit()
        resp['status'] = 201
        resp['message'] = 'Album created successfully'
        resp['album'] = {
            'album_id': album_seq[0],
            'album_name': album_name,
            'artist_name': artist_name
        }
    except Exception as e:
        transaction.rollback()
        logger.critical(e)
        resp['status'] = 500
        resp['message'] = 'Server Error'

    return make_response(resp)


@albums.route('/albums/<album_id>', methods=[PUT])
def update_albums(album_id):
    request_data = request.get_json(force=True)
    album_name = request_data.get("album_name")
    artist_name = request_data.get("artist_name")
    request_data.pop("album_id")
    artist = connection.execute("select artist_id from artist where artist_name=:artist_name", **{'artist_name': artist_name}).fetchone()
    if artist is None:
        insert = "INSERT INTO ARTIST(ARTIST_ID, ARTIST_NAME) values(artist_sequence.NEXTVAL, :artist_name)"
        row = connection.execute(insert, **{'artist_name': artist_name})
        query = "UPDATE ALBUM SET ALBUM_NAME=:album_name, ARTIST_ID=artist_sequence.CURRVAL where ALBUM_ID={}".format(album_id)
        row = connection.execute(query, **{'album_name': album_name})
    else:
        query = "UPDATE ALBUM SET ALBUM_NAME=:album_name, ARTIST_ID=:artist_id where ALBUM_ID={}".format(album_id)
        row = connection.execute(query, **{'album_name': album_name, 'artist_id': artist[0]})

    logger.info("SQL Query: {}".format(query))

    resp = {}
    try:
        resp['status'] = CREATED
        resp['message'] = 'Album updated successfully'
        resp['album'] = {
            'artist_name': artist_name,
            'album_name': album_name,
            'album_id': album_id
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
    album_params = set(request_data.keys())
    bad_params = album_params - OPT_PARAMS

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
