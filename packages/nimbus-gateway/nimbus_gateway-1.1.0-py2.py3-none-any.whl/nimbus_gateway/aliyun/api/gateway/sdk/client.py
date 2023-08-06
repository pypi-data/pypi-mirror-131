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
from dateutil import parser
from datetime import datetime
import requests
from nimbus_utils.utils import smart_bytes, smart_str
from .req import Request
from .constant import Method, HttpHeader, HttpMethod, SystemHeader, ContentType, HTTP_METHOD_MAP, \
    DEFAULT_TIMEOUT
from .utils import message, signature as sign_util


class DefaultClient:
    def __init__(self, app_key=None, app_secret=None, time_out=DEFAULT_TIMEOUT, verify=False):
        self.__app_key = app_key
        self.__app_secret = app_secret
        self.__time_out = time_out
        self.__verify = verify

    def __get_http_method(self, method):
        m = HTTP_METHOD_MAP.get(method, None)
        return m

    def _get_timestamp(self):
        return str(int(time.time() * 1000))

    def _get_nonce(self):
        return str(uuid.uuid4())

    def execute(self, req: Request = None):
        return self._request(req=req)

    def _request(self, req: Request = None):
        headers = self._build_headers(req=req)
        http_method = self.__get_http_method(req.get_method())
        url = "{host}{path}".format(host=req.get_host(), path=req.get_path())
        timeout = req.get_time_out() if req.get_time_out() > 0 else self.__time_out
        headers = {k: str(v) if v else None for k, v in headers.items() if v}
        params = req.get_query_str()
        if http_method == HttpMethod.POST:
            data = smart_bytes(req.get_body())
            resp = requests.post(url=url, headers=headers, data=data, params=params, timeout=timeout, verify=self.__verify)
        elif http_method == HttpMethod.PUT:
            data = smart_bytes(req.get_body())
            resp = requests.put(url=url, headers=headers, data=data, params=params, timeout=timeout, verify=self.__verify)
        elif http_method == HttpMethod.GET:
            resp = requests.get(url=url, headers=headers, params=params, timeout=timeout, verify=self.__verify)
        elif http_method == HttpMethod.DELETE:
            resp = requests.delete(url=url, headers=headers, params=params, timeout=timeout, verify=self.__verify)
        else:
            raise Exception("unsupported method:{}".format(req.get_method()))
        return resp

    def _build_headers(self, req: Request = None):
        headers = dict()
        header_params = req.get_headers()
        if header_params and isinstance(header_params, dict):
            headers.update(header_params)
        http_method = self.__get_http_method(req.get_method())
        headers[SystemHeader.X_CA_TIMESTAMP] = self._get_timestamp()
        headers[SystemHeader.X_CA_NONCE] = self._get_nonce()
        headers[SystemHeader.X_CA_KEY] = self.__app_key
        if req.get_stage():
            headers[SystemHeader.X_CA_STAGE] = req.get_stage()
        if req.get_content_type():
            headers[HttpHeader.HTTP_HEADER_CONTENT_TYPE] = req.get_content_type()
        else:
            headers[HttpHeader.HTTP_HEADER_CONTENT_TYPE] = ContentType.CONTENT_TYPE_JSON
        if HttpHeader.HTTP_HEADER_ACCEPT in header_params and header_params[HttpHeader.HTTP_HEADER_ACCEPT]:
            headers[HttpHeader.HTTP_HEADER_ACCEPT] = header_params[HttpHeader.HTTP_HEADER_ACCEPT]
        else:
            headers[HttpHeader.HTTP_HEADER_ACCEPT] = ContentType.CONTENT_TYPE_JSON
        body = req.get_body()
        if http_method in [HttpMethod.POST, HttpMethod.PUT]:
            headers[HttpHeader.HTTP_HEADER_CONTENT_MD5] = message.get_md5_base64_str(body)
        sign = sign_util.sign(secret=self.__app_secret, method=http_method, path=req.get_path(),
                              headers=headers, querys=req.get_query_str(),
                              bodys=body, customer_headers=req.get_sign_customer_headers())
        headers[SystemHeader.X_CA_SIGNATURE] = sign
        return headers

