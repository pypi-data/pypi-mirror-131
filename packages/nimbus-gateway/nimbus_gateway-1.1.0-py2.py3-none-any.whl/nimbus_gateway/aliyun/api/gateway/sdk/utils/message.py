# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import os
import json
import uuid
import time
import base64
import hashlib
from dateutil import parser
from datetime import datetime
from nimbus_utils.utils import smart_bytes, smart_str


def base64_data(data):
    """
    先进行MD5摘要再进行Base64编码获取摘要字符串
    :param data:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(smart_bytes(data))
    en_data = base64.encodebytes(md5.digest())
    return smart_str(en_data)


def _get_md5(content):
    m = hashlib.md5()
    m.update(content)
    return m.digest()


def get_md5_base64_str(content):
    content = smart_bytes(content)
    md5_bytes = base64.encodebytes(_get_md5(content)).strip()
    return smart_str(md5_bytes)


def utf8_to_iso88591(data, encoding="ISO-8859-1"):
    """
    UTF-8编码转换为ISO-9959-1
    :param data:
    :param encoding:
    :return:
    """
    data_bytes = smart_bytes(data)
    return data_bytes.decode(encoding)


def iso88591_to_utf8(data, encoding="ISO-8859-1"):
    """
    ISO-9959-1编码转换为UTF-8
    :param data:
    :param encoding:
    :return:
    """
    data_bytes = smart_bytes(data, encoding=encoding)
    return data_bytes.decode("UTF-8")


