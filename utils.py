import logging
import os
from mongolog import MongoHandler

if os.getenv('DEBUG'):
    DB = 'bid_debug'
else:
    DB = 'bid'

log = logging.getLogger('discord')
log.setLevel(logging.INFO)
log.addHandler(MongoHandler.to(db=DB, collection='logs', level=logging.INFO))
handler_stdout = logging.StreamHandler()
handler_stdout.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
log.addHandler(handler_stdout)
