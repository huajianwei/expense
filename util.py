#encoding: utf-8

import web
import config

def connect_db():
    return web.database(**config.db_conf)

def select_one(db, gid):
    return list(db.select(config.table, where='gid=%d' % int(gid)))[0]

def filter_readonly(input_dict):
    i = dict(input_dict)
    for key in i.keys():
        if key not in config.fields_conf or config.fields_conf[key]['readonly']:
            del i[key]
    return i

def get_remain(db):
    return list(db.select('money', what='money'))[0].money

def set_remain(db, money):
    db.update('money', where="1", money=money)

def incr_remain_by(db, money):
    db.update('money', where="1", money=web.SQLLiteral('money+(%f)' % money))

def change_remain(db, direction, amount, cancel = False):
    amount = -float(amount) if cancel else float(amount)
    if int(direction) == config.income:
        incr_remain_by(db, amount)
    else: #outcome
        incr_remain_by(db, -amount)
