#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/6 10:32
# @Author  : Adyan
# @File    : login.py


from flask import Flask, request
from flask_cors import CORS
from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from .cookies import Cookies
from ..config_mongo import settings
from ..Utils import ReidsClient

monkey.patch_all()
app = Flask(__name__)
app.config.update(
    DEBUG=True
)
CORS(app, supports_credentials=True)
set = settings.Settings


# TB_detail
@app.route('/cookie', methods=["post", "get"])
def detail():
    types = request.args.to_dict().get("type")
    host = request.args.to_dict().get("host")
    DB = request.args.to_dict().get("DB", 2)
    dl = request.args.to_dict().get("delete")
    login_url = request.args.to_dict().get("login_url", 'https://login.taobao.com/member/login.jhtml?')
    user = set(host=host).config
    res = ReidsClient({"HOST": host, 'DB': int(DB)}).redis_conn
    ip = request.remote_addr
    if dl:
        res.delete(ip)
    if res.exists(ip):
        res.setrange(ip, 0, int(res.get(ip)) + 1)
    else:
        res.set(ip, 0, ex=3600)
    code = int(res.get(ip))
    if int(res.get(ip)) == 0:
        res.set(types, Cookies().taobao_cookies(user.get(types), login_url))
        print(res.get(types))
        return {
            "code": code,
            "data": res.get(types).decode('utf-8'),
        }
    else:
        return {
            "code": code,
            "data": res.get(types).decode('utf-8'),
        }


def start(host, prot):
    """9090"""
    app.run(host=host, port=prot)
    http_server = WSGIServer((host, prot), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
