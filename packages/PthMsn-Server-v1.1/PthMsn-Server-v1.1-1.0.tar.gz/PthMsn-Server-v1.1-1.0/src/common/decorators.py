import datetime
import socket
import sys
import logging

sys.path.append('../../')

LOGGER = logging.getLogger('server')


def logger(log_func):
    """
    A decorator that logs function calls.
    Saves debug events containing
    information about the name of the called function, the parameters with which
    the function is called, and the module is calling the function.
    :param log_func:
    :return:
    """
    def log_saver(*args, **kwargs):
        result = log_func(*args, **kwargs)
        LOGGER.debug(f'{datetime.datetime.now()}. Function {log_func.__name__} is called from module {log_func.__module__}', stacklevel=2)
        return result
    return log_saver


def login_required(func):
    """
    A decorator that verifies that the client is authorized on the server.
    Checks that the passed socket object is in
    the list of authorized clients.
    Except for passing the dictionary-query
    for authorization. If the client is not authorized,
    throws a TypeError exception.
    :param func:
    :return:
    """
    def checker(*args, **kwargs):
        from ServerAPP.server_start import Server
        from ServerAPP.common.variables import ACTION, PRESENCE
        if isinstance(args[0], Server):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True
            for arg in args:
                if isinstance(arg, dict) and ACTION in arg and arg[ACTION] == PRESENCE:
                    found = True
            if not found:
                raise TypeError
        return func(*args, **kwargs)
    return checker
