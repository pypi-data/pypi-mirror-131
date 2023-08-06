# !/usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author: Wang Ye (Wayne)
@file: tt_api.py
@time: 2021/05/29
@contact: wangye@oppo.com
@site: 
@software: PyCharm
# code is far away from bugs.
"""

import collections
import requests
import socket
from hashlib import md5
from datetime import datetime
from urllib.parse import urljoin


class TT_API:
    def __init__(self, to_users=[], from_user='health-algorithm'):
        self._appid = from_user
        self._secret = {
            'health-algorithm': '223d0590a25a47cea1385197ad31ad81',
            'health-data': '7c77496167924d4e9581d44c7dc8987a'
        }[from_user]
        self._host = 'https://ttapi.myoas.com'
        self._headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Response-Type": "application/json"
        }
        self._to_users = to_users

    def __sign(self, path: str, payload: dict) -> str:
        flag = "_tt_"
        params_list = [path]
        payload_sorted = collections.OrderedDict(sorted(payload.items()))
        list(map(lambda x: params_list.append(x[0] + "=" + str(x[1])), payload_sorted.items()))
        params_list.append(self._secret)
        result = f"{flag}".join(params_list)
        # print(f"待签名字符串: {result}")
        return md5(result.encode('utf-8')).hexdigest()

    def send_text(self, content: str, to_users=[]):
        if to_users:
            self._to_users = to_users
        api_path = '/s/api/message/notification/send'
        payload = {
            'appid': self._appid,
            'time': int(datetime.now().timestamp()),
            'from_user': self._appid,
            'to_users': ','.join(self._to_users),
            'msg_content': f'[{socket.gethostname()}]: {content}',
            'msg_type': '1'
        }
        payload.update({
            'sign': self.__sign(api_path, payload)
        })
        resp = requests.post(url=urljoin(self._host, api_path), headers=self._headers, data=payload)
        # print(resp.text)
		return resp
