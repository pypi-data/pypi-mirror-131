#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2021/12/15 1:49 下午
# @Author  : Hubert Shelley
# @Project  : starlette_utils
# @FileName: json.py
# @Software: PyCharm
"""
import datetime
import json
import uuid


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, uuid.UUID):
            return obj.__str__()
        else:
            return json.JSONEncoder.default(self, obj)


def json2str(dictionary):
    """
    将包含时间对象的字典转换成json字符串
    :return:
    """
    return json.dumps(dictionary, cls=JsonEncoder)


def object_to_dict(obj):
    """
    将对象转换成字典
    :return:
    """
    if type(obj) is dict:
        return obj
    if type(obj) is str:
        return obj
    if type(obj) is bytes:
        return obj
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


def str2dict(string):
    # return eval(string)
    return json.loads(string.replace("'", "\""))
