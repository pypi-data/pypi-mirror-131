import sys
import json
from ServerAPP.common.variables import MAX_PKG, ENCODING
from ServerAPP.common.decorators import logger
sys.path.append('../../')


@logger
def get_message(client):
    """
    Get message from socket function.
    :param client:
    :return:
    """
    encoded_response = client.recv(MAX_PKG)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


@logger
def send_message(sock, message):
    """
    Send message for socket function.
    :param sock:
    :param message:
    :return:
    """
    json_req = json.dumps(message)
    package_to_send = json_req.encode(ENCODING)
    sock.send(package_to_send)
