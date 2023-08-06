#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time:    2021-12-15 01:40
# @Author:  geng
# @Email:   yonglonggeng@163.com
# @WeChat:  superior_god
# @File:    web.py
# @Project: BoxJellyfish
import time

from flask import Flask, request, jsonify

from resultStages.UserInterFace import *

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

app = Flask(__name__)
userModel = UserModel()
userModel.load_model()


# =========================================
def event_api(data):
    with graph.as_default():
        set_session(sess)
        res = userModel.predict(data)
    return res


def is_tf():
    with open("resultStages/BJF.json", 'r') as load_f:
        load_dict = json.load(load_f)

    return load_dict['framework'] == 'tf'


# =========================================
@app.route('/invocations', methods=['POST'])
def event_extraction():
    data = request.get_json()
    if is_tf():
        res = event_api(data)
    else:
        res = userModel.predict(data)
    result = {
        "status": 0,
        "msg": "接口成功连接。" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        "data": res,
        "Info": "BDA-API"
    }

    return jsonify(result)


# if __name__ == "__main__":
app.run(host='0.0.0.0', port=8888)
