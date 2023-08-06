import logging


LOG_FILE = 'ClientAPP/log/client_logs/client.log'
LOG = logging.getLogger('client')
LOG_FORMAT = logging.Formatter('%(asctime)-s %(levelname)-s %(module)-s %(message)s')
FILE_HANDLER = logging.FileHandler(LOG_FILE, encoding='utf-8')
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(LOG_FORMAT)
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)
