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
tracks = Blueprint('tracks', __name__, url_prefix='/api/v1')
logger = logging.getLogger('app')


@tracks.route('/tracks', methods=[GET])
def list_albums():
    rows = connection.execute("SELECT T.TRACK_ID, T.TRACK_NAME, TO_DATE(T.CREATED_AT, 'DD-MON-YY'), T.TRACK_NUM, B.ALBUM_NAME, B.ALBUM_ID, A.ARTIST_NAME, A.ARTIST_ID FROM TRACK T JOIN ALBUM B ON (T.ALBUM_ID = B.ALBUM_ID) JOIN ARTIST A ON (T.ARTIST_ID = A.ARTIST_ID)").fetchall();
    resp = {'status': HTTP_200_OK, 'tracks': []}
    for row in rows:
        track_info = {
            'track_id': row[0],
            'track_name': row[1],
            'created_at': row[2].strftime('%d-%b-%Y'),
            'track_num': row[3],
            'album_name': row[4],
            'album_id': row[5],
            'artist_name': row[6],
            'artist_id': row[7]
        }
        resp['tracks'].append(track_info)

    return make_response(resp)


@tracks.route('/tracks/<track_id>', methods=[GET])
def get_tracks(track_id):
    try:
        track_id = int(track_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid track ID: {}'.format(track_id)
        }
        return make_response(resp)

    query = "SELECT T.TRACK_ID, T.TRACK_NAME, TO_DATE(T.CREATED_AT, 'DD-MON-YY'), T.TRACK_NUM, B.ALBUM_NAME, B.ALBUM_ID, A.ARTIST_NAME, A.ARTIST_ID FROM TRACK T JOIN ALBUM B ON (T.ALBUM_ID = B.ALBUM_ID) JOIN ARTIST A ON (T.ARTIST_ID = A.ARTIST_ID) WHERE TRACK_ID = {}".format(track_id)
    row = connection.execute(query).fetchone()
    resp = {'status': 200, 'album': {}}
    track_info = {
        'track_id': row[0],
        'track_name': row[1],
        'created_at': row[2].strftime('%d-%b-%Y'),
        'track_num': row[3],
        'album_name': row[4],
        'album_id': row[5],
        'artist_name': row[6],
        'artist_id': row[7]
    }
    resp['track'] = track_info

    return make_response(resp)


@tracks.route('/tracks/<track_id>', methods=[DELETE])
def delete_tracks(track_id):
    try:
        track_id = int(track_id)
    except ValueError:
        resp = {
            'status': 400,
            'error': 'Invalid track ID: {}'.format(track_id)
        }
        return make_response(resp)

    query = "DELETE FROM TRACK WHERE TRACK_ID = {}".format(track_id)
    row = connection.execute(query)
    resp = {
        'status': 200,
        'message': 'Track ID: {} deleted successfully'.format(track_id)
    }

    return make_response(resp)

@tracks.route('/tracks', methods=[POST])
def create_tracks():
    request_data = request.get_json(force=True)
    track_name = request_data.get("track_name")
    created_at = request_data.get("created_at")
    track_num = request_data.get("track_num")
    album_id = request_data.get("album_id")
    artist_id = request_data.get("artist_id")
    album_name = request_data.get("album_name")
    artist_name = request_data.get("artist_name")
    request_data.pop("track_id")

    resp = {}
    transaction = connection.begin()
    try:
        artist = connection.execute("select artist_id from artist where artist_name=:artist_name", **{'artist_name': artist_name}).fetchone()
        album = connection.execute("select album_id from album where album_name=:album_name", **{'album_name': album_name}).fetchone()
        if artist is None and album is None:
            insert = "INSERT INTO ARTIST(ARTIST_ID, ARTIST_NAME) values(artist_sequence.NEXTVAL, :artist_name)"
            row = connection.execute(insert, **{'artist_name': artist_name})
            artist_seq = connection.execute('SELECT artist_sequence.CURRVAL FROM DUAL').fetchone()
            insert = "INSERT INTO ALBUM(ALBUM_ID, ALBUM_NAME, ARTIST_ID) values(album_sequence.NEXTVAL, :album_name, artist_sequence.CURRVAL)"
            row = connection.execute(insert, **{'album_name': album_name})
            artist_seq = connection.execute('SELECT album_sequence.CURRVAL FROM DUAL').fetchone()
            query = "INSERT INTO TRACK (TRACK_NAME, CREATED_AT, TRACK_NUM, ALBUM_ID, ARTIST_ID, TRACK_ID) VALUES (:track_name, TO_DATE(:created_at, 'DD-MON-YY'), :track_num, album_sequence.CURRVAL, artist_sequence.CURRVAL, track_sequence.NEXTVAL)"
            row = connection.execute(query, **{'track_name': track_name, 'created_at': created_at, 'track_num': track_num, })
        elif artist is None and album is not None:
            insert = "INSERT INTO ARTIST(ARTIST_ID, ARTIST_NAME) values(artist_sequence.NEXTVAL, :artist_name)"
            row = connection.execute(insert, **{'artist_name': artist_name})
            artist_seq = connection.execute('SELECT artist_sequence.CURRVAL FROM DUAL').fetchone()
            update_album = "UPDATE ALBUM SET ARTIST_ID=:artist_id WHERE album_id={}".format(album[0])
            row = connection.execute(update_album, **{'artist_id': artist_seq[0]})
            query = "INSERT INTO TRACK (TRACK_NAME, CREATED_AT, TRACK_NUM, ALBUM_ID, ARTIST_ID, TRACK_ID) VALUES (:track_name, TO_DATE(:created_at, 'DD-MON-YY'), :track_num, :album_id, :artist_id, track_sequence.NEXTVAL)"
            row = connection.execute(query, **{'track_name': track_name, 'created_at': created_at, 'track_num': track_num, 'artist_id': artist_seq[0], 'album_id': album[0]})
        elif artist is not None and album is None:
            insert = "INSERT INTO ALBUM(ALBUM_ID, ALBUM_NAME, ARTIST_ID) values(album_sequence.NEXTVAL, :album_name, :artist_id)"
            row = connection.execute(insert, **{'album_name': album_name, 'artist_id': artist[0]})
            query = "INSERT INTO TRACK (TRACK_NAME, CREATED_AT, TRACK_NUM, ALBUM_ID, ARTIST_ID, TRACK_ID) VALUES (:track_name, TO_DATE(:created_at, 'DD-MON-YY'), :track_num, album_sequence.CURRVAL, :artist_id, track_sequence.NEXTVAL)"
            row = connection.execute(query,**{'track_name': track_name, 'created_at': created_at, 'track_num': track_num,'artist_id': artist[0]})
        else:
            query = "INSERT INTO TRACK (TRACK_NAME, CREATED_AT, TRACK_NUM, ALBUM_ID, ARTIST_ID, TRACK_ID) VALUES (:track_name, TO_DATE(:created_at, 'DD-MON-YY'), :track_num, :album_id, :artist_id, track_sequence.NEXTVAL)"
            row = connection.execute(query,**{'track_name': track_name, 'created_at': created_at, 'track_num': track_num, 'album_id': album[0],'artist_id': artist[0]})

        track_seq = connection.execute('SELECT track_sequence.CURRVAL FROM DUAL').fetchone()
        transaction.commit()

    #query = "INSERT INTO TRACK (TRACK_NAME, CREATED_AT, TRACK_NUM, ALBUM_ID, ARTIST_ID, TRACK_ID) VALUES (:track_name, TO_DATE(:created_at, 'DD-MON-YY'), :track_num, :album_id, :artist_id, track_sequence.NEXTVAL)"
    #status = connection.execute(query, **request_data)
        resp['status'] = 201
        resp['message'] = 'Track created successfully'
        resp['track'] = {
            'track_id': track_seq[0],
            'track_name': track_name,
            'created_at': created_at,
            'track_num': track_num,
            'album_id': album_id,
            'artist_id': artist_id,
            'album_name': album_name,
            'artist_name': artist_name
        }
    except Exception as e:
        transaction.rollback()
        logger.critical(e)
        resp['status'] = INTERNAL_SERVER_ERROR
        resp['message'] = 'Server Error'

    return make_response(resp)


@tracks.route('/tracks/<track_id>', methods=[PUT])
def update_tracks(track_id):
    request_data = request.get_json(force=True)
    track_name = request_data.get("track_name")
    created_at = request_data.get("created_at")
    track_num = request_data.get("track_num")
    album_id = request_data.get("album_id")
    artist_id = request_data.get("artist_id")
    request_data.pop("track_id")
    request_data.pop("artist_name")
    request_data.pop("album_name")
    query = "UPDATE TRACK SET TRACK_NAME=:track_name, CREATED_AT=TO_DATE(:created_at, 'DD-MON-YY'), TRACK_NUM=:track_num, ALBUM_ID=:album_id, ARTIST_ID=:artist_id where TRACK_ID={}".format(track_id)
    logger.info("SQL Query: {}".format(query))

    resp = {}
    try:
        status = connection.execute(query, **request_data)
        resp['status'] = CREATED
        resp['message'] = 'Track updated successfully'
        resp['track'] = {
            'track_name': track_name,
            'created_at': created_at,
            'track_num': track_num,
            'album_id': album_id,
            'artist_id': album_id,
            'track_id': track_id
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
