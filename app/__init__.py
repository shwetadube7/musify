import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from flask_jsonschema import JsonSchema, ValidationError


# Define the WSGI application object
app = Flask(__name__)
CORS(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# JSONSchema
#jsonschema = JsonSchema(app)


@app.errorhandler(ValidationError)
def on_jsonschema_validation_error(e):
    return jsonify(dict(message=e.message)), 400


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify(dict(message='Not Found')), 404


def register_blueprints(app):
    # Import a module / component using its blueprint handler variable
    from app.users.routes import users as user_module
    # Register blueprint(s)
    app.register_blueprint(user_module)
    # app.register_blueprint(xyz_module)
    from app.artists.routes import artists as artist_module
    app.register_blueprint(artist_module)
    from app.albums.routes import albums as album_module
    app.register_blueprint(album_module)
    from app.tracks.routes import tracks as track_module
    app.register_blueprint(track_module)
    # ..



register_blueprints(app)

# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()

# Setup logging

base_format = '%(asctime)s %(funcName)s [%(levelname)s]:%(message)s'
logging.basicConfig(
    format=base_format,
    level=logging.INFO
)
logger = logging.getLogger('app')
MEGA_BYTE = 1000000
rotate_handler = RotatingFileHandler(
    app.config['LOGGING_FILE'],
    maxBytes=10 * MEGA_BYTE,
    backupCount=5
)
rotate_handler.setFormatter(
    Formatter(
        base_format + ' (file %(filename)s, function %(funcName)s:%(lineno)d)'
    )
)
rotate_handler.setLevel(logging.INFO)

logging.getLogger().addHandler(rotate_handler)
