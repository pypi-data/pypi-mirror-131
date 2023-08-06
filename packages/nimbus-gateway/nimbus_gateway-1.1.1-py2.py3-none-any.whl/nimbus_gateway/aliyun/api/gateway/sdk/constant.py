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

__all__ = [
    "HttpHeader",
    "ContentType",
    "HttpMethod",
    "SystemHeader",
    "Method",
    'DEFAULT_TIMEOUT',
    "HTTP_METHOD_MAP",
]


# //签名算法HmacSha256
HMAC_SHA256 = "HmacSHA256"
# //编码UTF-8
ENCODING = "UTF-8"
# //UserAgent
USER_AGENT = "demo/aliyun/java"
# //换行符
LF = "\n"
# //串联符
SPE1 = ","
# //示意符
SPE2 = ":"
# //连接符
SPE3 = "&"
# //赋值符
SPE4 = "="
# //问号符
SPE5 = "?"
# //默认请求超时时间,单位毫秒
DEFAULT_TIMEOUT = 1000
# //参与签名的系统Header前缀,只有指定前缀的Header才会参与到签名中
CA_HEADER_TO_SIGN_PREFIX_SYSTEM = "X-Ca-"


class HttpHeader(object):
    """
    HTTP头常量
    """
    # //请求Header Accept
    HTTP_HEADER_ACCEPT = "Accept"
    # //请求Body内容MD5 Header
    HTTP_HEADER_CONTENT_MD5 = "Content-MD5"
    # //请求Header Content-Type
    HTTP_HEADER_CONTENT_TYPE = "Content-Type"
    # //请求Header UserAgent
    HTTP_HEADER_USER_AGENT = "User-Agent"
    # //请求Header Date
    HTTP_HEADER_DATE = "Date"


class SystemHeader(object):
    """
    系统HTTP头常量
    """
    # //签名Header
    X_CA_SIGNATURE = "X-Ca-Signature"
    # //所有参与签名的Header
    X_CA_SIGNATURE_HEADERS = "X-Ca-Signature-Headers"
    # //请求时间戳
    X_CA_TIMESTAMP = "X-Ca-Timestamp"
    # //请求放重放Nonce,15分钟内保持唯一,建议使用UUID
    X_CA_NONCE = "X-Ca-Nonce"
    # //APP KEY
    X_CA_KEY = "X-Ca-Key"
    # //X-Ca-Stage
    X_CA_STAGE = "X-Ca-Stage"


class ContentType(object):
    """
    常用HTTP Content-Type常量
    """
    # //表单类型Content-Type
    CONTENT_TYPE_FORM = "application/x-www-form-urlencoded"
    # // 流类型Content-Type
    CONTENT_TYPE_STREAM = "application/octet-stream"
    # //JSON类型Content-Type
    CONTENT_TYPE_JSON = "application/json"
    # //XML类型Content-Type
    CONTENT_TYPE_XML = "application/xml"
    # //文本类型Content-Type
    CONTENT_TYPE_TEXT = "application/text"


class HttpMethod(object):
    """
    HTTP方法常量
    """
    # //GET
    GET = "GET"
    # //POST
    POST = "POST"
    # //PUT
    PUT = "PUT"
    # //DELETE
    DELETE = "DELETE"


class Method(object):
    GET = "GET"
    POST_FORM = "POST_FORM"
    POST_STRING = "POST_STRING"
    POST_BYTES = "POST_BYTES"
    PUT_FORM = "PUT_FORM"
    PUT_STRING = "PUT_STRING"
    PUT_BYTES = "PUT_BYTES"
    DELETE = "DELETE"


HTTP_METHOD_MAP = {
    Method.GET: HttpMethod.GET,
    Method.POST_FORM: HttpMethod.POST,
    Method.POST_STRING: HttpMethod.POST,
    Method.POST_BYTES: HttpMethod.POST,
    Method.PUT_FORM: HttpMethod.PUT,
    Method.PUT_STRING: HttpMethod.PUT,
    Method.PUT_BYTES: HttpMethod.PUT,
    Method.DELETE: HttpMethod.DELETE,
}
