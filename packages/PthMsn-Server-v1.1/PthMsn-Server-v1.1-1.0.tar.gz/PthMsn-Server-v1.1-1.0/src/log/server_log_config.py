import logging.handlers


LOG_FILE = 'ServerAPP/log/server_logs/server.log'
LOG = logging.getLogger('server')
LOG_FORMAT = logging.Formatter('%(asctime)-s %(levelname)-s %(module)-s %(message)s')
FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(filename=LOG_FILE, when='D', interval=1, delay=True)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(LOG_FORMAT)
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)
