# Pagination Parameters
TOTAL = 'total'
LIMIT = 'limit'
OFFSET = 'offset'
MAX_LIMIT = 100


# HTTP Methods
GET = 'GET'
PUT = 'PUT'
POST = 'POST'
PATCH = 'PATCH'
DELETE = 'DELETE'


# HTTP Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_409_CONFLICT = 409
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_400_CLIENT_ERROR = 400
HTTP_500_INTERNAL_SERVER_ERROR = 500


# Response Status
INSUFFICIENT_PERMISSIONS = 'Insufficient Permissions'
INTERNAL_SERVER_ERROR = 'Internal Server Error'
CONFLICT = 'Conflict'
NOT_FOUND = 'Not Found'
FORBIDDEN = 'Forbidden'
CLIENT_ERROR = 'Client Error'
CREATED = 'Created'
DELETED = 'Deleted'
OK = 'Ok'


# Additional
STATUS = 'status'
MESSAGE = 'message'
LIST_OPT_PARAMS = frozenset([LIMIT, OFFSET, 'gender'])
SEARCH_OPT_PARAMS = frozenset([
    LIMIT, OFFSET, 'last_name', 'first_name', 'name', 'npi'
])
