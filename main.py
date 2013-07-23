#!/usr/bin/python
#encoding: utf-8

import os
import sys
import copy
import time

import web
web.config.debug = False

import util
import config

urls = [
    '/'     ,           'main',
    '/list',            'Lister',
    '/insert',          'Inserter',
    '/edit/(.*)',       'Editor',
    '/remove/(.*)/.*',  'Remover',
    '/login',           'Login',
    '/logout',          'Logout',
]

app = web.application(urls, globals())

#render: add builtin and itself
render_globals = __builtins__.copy() if isinstance(__builtins__, dict) else __builtins__.__dict__.copy()
render = web.template.render(config.template_dir, cache=False, globals = render_globals)
render_globals['render'] = render
render_globals['time'] = time

if config.need_log:
    import logging
    logging.basicConfig(**config.log_conf)

if config.need_login:
    web.config.debug = False #session just won't work with debug mode
    session = web.session.Session(app, web.session.DiskStore(config.session_dir), initializer={'login': False})


class BaseHandler(object):
    def __init__(self):
        pass

class main(BaseHandler):
    def GET(self):
        web.seeother('/list')


class Lister(BaseHandler):
    def GET(self):
        i = web.input(page = '1')
        page = int(i.page) if int(i.page) > 0 else 1
        db = util.connect_db()
        nr_records = list(db.select(config.table, what='count(1) as count'))[0].count
        pages = (nr_records + config.nr_items - 1) / config.nr_items
        offset = (page - 1) * config.nr_items
        rows = list(db.select(config.table, order='gid desc', offset=offset, limit=config.nr_items))
        remain = util.get_remain(db)
        del db
        return render.list(rows, page, pages, config.fields, remain)


class Inserter(BaseHandler):
    def GET(self):
        return render.editor(config.fields, '/insert', '')

    def POST(self):
        i = util.filter_readonly(web.input())
        db = util.connect_db()
        trans = db.transaction()
        try:
            util.change_remain(db, i['direction'], i['amount'], cancel = False)
            i['remain'] = util.get_remain(db)
            gid = db.insert(config.table, **i)
        except Exception, e:
            trans.rollback()
            logging.warn('insert failed: %s\n%s', str(e), str(i))
            return render.msg('insert failed')
        else:
            trans.commit()
        logging.info('insert: %s', str(i))
        del db
        web.seeother('/edit/%d?msg=ok' % gid)


class Editor(BaseHandler):
    def GET(self, gid):
        db = util.connect_db()
        row = util.select_one(db, gid)
        fields = copy.deepcopy(config.fields)
        for item in fields:
            item[-1] = row[item[0]]
        del db
        return render.editor(fields, '/edit/' + gid, web.input(msg='').msg)

    def POST(self, gid):
        i = util.filter_readonly(web.input())
        db = util.connect_db()
        trans = db.transaction()
        try:
            #还原余额
            orig = util.select_one(db, gid)
            util.change_remain(db, orig['direction'], orig['amount'], cancel=True)
            #更新余额
            util.change_remain(db, i['direction'], i['amount'], cancel = False)
            i['remain'] = util.get_remain(db)
            db.update(config.table, where='gid=%d'%int(gid), **i)
        except Exception, e:
            trans.rollback()
            logging.warn('edit failed: %s\n%s', str(e), str(i))
            return render.msg('edit failed')
        else:
            trans.commit()
        del db
        logging.info('edit:\n%s\n%s', str(orig), str(i))
        web.seeother('/edit/' + gid + '?msg=ok')


class Remover(BaseHandler):
    def GET(self, gid):
        web.header('Cache-Control', 'no-cache')
        db = util.connect_db()
        trans = db.transaction()
        try:
            #还原余额
            orig = util.select_one(db, gid)
            util.change_remain(db, orig['direction'], orig['amount'], cancel=True)
            db.delete(config.table, where='gid=%d'%int(gid))
        except Exception, e:
            trans.rollback()
            logging.warn('remove failed: %s\n%s', str(e), str(i))
            return render.msg('remove failed')
        else:
            trans.commit()
        del db
        logging.info('remove: %s', str(orig))
        return render.msg('删除成功')

 
class Login(BaseHandler):
    def GET(self):
        i = web.input(return_url='/', msg='')
        return render.login(i.return_url, i.msg)

    def POST(self):
        i = web.input(return_url='/', msg='')
        if config.user_conf.get(i.username) == i.password:
            session.login = True
            print 'login ok'
            web.seeother(i.return_url)
        else:
            return render.login(i.return_url, '用户名/密码错误')


class Logout(BaseHandler):
    def GET(self):
        session.login = False
        web.seeother("/login")


def login_hook(handler):
    path_info = web.ctx.env['PATH_INFO']
    if path_info != '/login' and not session.login:
        uri = web.ctx.env['REQUEST_URI']
        web.seeother('/login?return_url=' + web.urlquote(uri))
    else:
        return handler()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.argv.append(str(config.port))

    if config.need_login:
        app.add_processor(login_hook)

    app.run()
    logging.debug('Server Started')
