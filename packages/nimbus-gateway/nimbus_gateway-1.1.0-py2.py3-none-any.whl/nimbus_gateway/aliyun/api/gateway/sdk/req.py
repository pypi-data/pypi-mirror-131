# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import os
import json
import uuid
import time
import base64
import hashlib
import logging
from typing import Any

from dateutil import parser
from datetime import datetime
from nimbus_gateway.aliyun.api.gateway.sdk.constant import Method, ContentType, DEFAULT_TIMEOUT


class Request(object):
    
    """
    （必选）请求方法
    """
    __method: Method
    """
    （必选）Host
    """
    __host: str
    """
    （必选）Path
    """
    __path: str
    """
    （可选）HTTP头
    """
    __headers: dict
    """
    （可选）BODY [FORM/STRING/BYTES] 
    """
    __body: Any
    """
    （可选）QUERY
    """
    __query_str: Any
    """
    （可选）ContentType
    """
    __content_type: ContentType.CONTENT_TYPE_JSON
    """
    （可选）TIMEOUT
    """
    __time_out: DEFAULT_TIMEOUT
    """
    （可选）目前支持 TEST、PRE、RELEASE 三个Stage，大小写不敏感，API提供者可以选择发布到哪个Stage，
    只有发布到指定Stage后API才可以调用，否则会提示API找不到或InvalidUrl。
    """
    __stage: str
    """
    （可选）自定义参与签名Header
    """
    __customer_sign_headers: list

    def __init__(self, host=None, path=None, method: Method = Method.POST_STRING, time_out=DEFAULT_TIMEOUT, headers={}):
        self.__method = method
        self.__host = host
        self.__path = path
        self.__headers = headers
        self.__time_out = time_out
        self.__body = None
        self.__query_str = None
        self.__content_type = None

    def __getattr__(self, name):
        if name not in self.__dict__:
            return None
        return super().__getattr__(name)

    def get_stage(self):
        return self.__stage

    def set_stage(self, stage):
        self.__stage = stage

    def get_method(self):
        return self.__method

    def set_method(self, method):
        self.__method = method

    def get_host(self):
        return self.__host

    def set_host(self, host):
        self.__host = host

    def get_path(self):
        return self.__path

    def set_path(self, path):
        self.__path = path

    def get_time_out(self):
        return self.__time_out

    def set_time_out(self, time_out):
        self.__time_out = time_out

    def get_content_type(self):
        return self.__content_type

    def set_content_type(self, content_type):
        self.__content_type = content_type

    def get_headers(self):
        return self.__headers

    def set_headers(self, headers={}):
        self.__headers = headers

    def get_query_str(self):
        return self.__query_str

    def set_query_str(self, query_str=None):
        self.__query_str = query_str

    def set_body(self, body):
        self.__body = body

    def get_body(self):
        return self.__body

    def get_sign_customer_headers(self):
        return self.__customer_sign_headers

    def set_sign_customer_headers(self, customer_sign_headers):
        self.__customer_sign_headers = customer_sign_headers




