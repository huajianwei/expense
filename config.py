#encoding: utf-8

import logging

debug = True

port = 9999

data_dir = 'data/'

session_dir  = 'session/'

template_dir = 'view/'
template_cache = False

need_log = True
log_conf = {
    'filename'  : 'web.log',
    'level'     : logging.DEBUG,
    'format'    : '[%(asctime)s] %(levelname)s: %(message)s',
    'datefmt'   : '%Y-%m-%d %H:%M:%S',
}

need_db = True
db_conf = {
    'dbn': 'sqlite',
    'db'  : data_dir + 'expense.db',
}
table = 'expense'

try:
    from local_config import *
except Exception, e:
    print 'import local_config failed', str(e)
    pass
