# DEFAULT VALUES
DEF_PORT = 7788
DEF_IP = '127.0.0.1'

# COMMON VARIABLES
MAX_CON = 5
MAX_PKG = 1024
ENCODING = 'utf-8'

# JIM VARIABLES
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
SENDER = 'sender'
DESTINATION = 'destination'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
EXIT = 'exit'
GET_FRIENDS = 'get_friends'
LIST_INFO = 'data_list'
REMOVE_FRIEND = 'remove'
ADD_FRIEND = 'add'
USERS_REQUEST = 'get_users'
DATA = 'bin'
ERROR = 'error'
PUBLIC_KEY = 'pubkey'
PUBLIC_KEY_REQUEST = 'pubkey_need'

RESP_OK = {RESPONSE: 200}
RESP_202 = {RESPONSE: 202, LIST_INFO: None}
RESP_BAD = {RESPONSE: 400, ERROR: 'Bad Request'}
RESP_205 = {RESPONSE: 205}
RESP_511 = {RESPONSE: 511, DATA: None}

DB_ENGINE = 'sqlite:///server_base.db3'