import os


# Statement for enabling the development environment
DEBUG = True

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database Connection Info
SQLALCHEMY_DATABASE_URI = 'oracle://lab:lab@127.0.0.1:1521/xe'
SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Logging path
LOGGING_FILE = os.path.join(BASE_DIR, 'app.log')

# JSONSchema
#JSONSCHEMA_DIR = os.path.join(BASE_DIR, 'jsonschema')
