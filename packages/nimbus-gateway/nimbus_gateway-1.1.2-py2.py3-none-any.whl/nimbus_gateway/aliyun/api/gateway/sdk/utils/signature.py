# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import os
import json
import uuid
import time
import base64
import hashlib
import hmac
from dateutil import parser
from datetime import datetime
from nimbus_gateway.aliyun.api.gateway.sdk import constant
from nimbus_gateway.aliyun.api.gateway.sdk.constant import *
from nimbus_utils.utils import smart_bytes, smart_str


def sign_hmac(source, secret):
    h = hmac.new(secret.encode(), source.encode(), hashlib.sha256)
    signature = base64.encodebytes(h.digest()).strip()
    signature = smart_str(signature)
    return signature


def sign_hmac_o(source, secret):
    message = smart_bytes(source)
    secret = smart_bytes(secret)
    h = hmac.new(secret, message, hashlib.sha256)
    signature = base64.encodebytes(h.digest()).strip()
    signature = smart_str(signature)
    return signature


def sign(secret: str, method: str, path: str, headers: dict, querys: dict, bodys: dict, customer_headers: list) -> str:
    """
    计算签名
    :param secret:
    :param method:
    :param path:
    :param headers:
    :param querys:
    :param bodys:
    :param customer_headers:
    :return:
    """
    message = build_sign_str(method, path, headers, querys, bodys, customer_headers)
    signature = sign_hmac_o(source=message, secret=secret)
    return signature


def build_sign_str(method: str, path: str, headers: dict, querys: dict, bodys: dict, customer_headers: list) -> str:
    """
    构建待签名字符串
    :param method:
    :param path:
    :param headers:
    :param querys:
    :param bodys:
    :param customer_headers:
    :return:
    """
    string_to_sign = [method.upper(), constant.LF]

    if HttpHeader.HTTP_HEADER_ACCEPT in headers and headers.get(HttpHeader.HTTP_HEADER_ACCEPT):
        string_to_sign.append(headers.get(HttpHeader.HTTP_HEADER_ACCEPT))

    string_to_sign.append(constant.LF)
    if HttpHeader.HTTP_HEADER_CONTENT_MD5 in headers and headers.get(HttpHeader.HTTP_HEADER_CONTENT_MD5):
        string_to_sign.append(headers.get(HttpHeader.HTTP_HEADER_CONTENT_MD5))

    string_to_sign.append(constant.LF)
    if HttpHeader.HTTP_HEADER_CONTENT_TYPE in headers and headers.get(HttpHeader.HTTP_HEADER_CONTENT_TYPE):
        string_to_sign.append(headers.get(HttpHeader.HTTP_HEADER_CONTENT_TYPE))

    string_to_sign.append(constant.LF)
    if HttpHeader.HTTP_HEADER_DATE in headers and headers.get(HttpHeader.HTTP_HEADER_DATE):
        string_to_sign.append(headers.get(HttpHeader.HTTP_HEADER_DATE))

    string_to_sign.append(constant.LF)
    string_to_sign.append(_build_headers(headers, customer_headers))
    string_to_sign.append(_build_resource(path, querys, bodys))
    return ''.join(string_to_sign)


def _build_resource(path: str, querys: dict, bodys: dict) -> str:
    """
    构建待签名Path+Query+BODY
    :param path:
    :param querys:
    :param bodys:
    :return:
    """
    sb = "" + path if path else ""
    sort_map = {}
    if querys and isinstance(querys, dict):
        for k, v in querys.items():
            if k:
                sort_map[k] = v
    if bodys and isinstance(bodys, dict):
        for k, v in bodys.items():
            if k:
                sort_map[k] = v
    sb_param = ""
    for k, v in sort_map.items():
        if not k:
            continue
        if len(sb_param) > 0:
            sb_param = sb_param + constant.SPE3
        sb_param = sb_param + k
        if v:
            sb_param = sb_param + constant.SPE4 + v
    if sb_param:
        sb = sb + constant.SPE5 + sb_param
    return sb


def _build_headers(headers: dict, customer_headers: list) -> str:
    """
    构建待签名Http头
    :param headers:
    :param customer_headers:
    :return:
    """

    unsign_headers = [
        SystemHeader.X_CA_SIGNATURE, HttpHeader.HTTP_HEADER_ACCEPT,
        HttpHeader.HTTP_HEADER_CONTENT_MD5, HttpHeader.HTTP_HEADER_CONTENT_TYPE,
        HttpHeader.HTTP_HEADER_DATE,
    ]
    signature_headers = []
    temp_headers = []
    if customer_headers:
        signed_headers = [h for h in customer_headers if h not in unsign_headers]
        signed_headers.sort()
        for k in signed_headers:
            v = headers.get(k)
            temp_headers.append(k)
            temp_headers.append(":")
            temp_headers.append(str(v))
            temp_headers.append(constant.LF)
            signature_headers.append(k)
        headers[SystemHeader.X_CA_SIGNATURE_HEADERS] = constant.SPE1.join(signature_headers)
    else:
        signed_headers = [h for h in headers.keys() if h not in unsign_headers]
        signed_headers.sort()
        for k in signed_headers:
            if k.startswith(constant.CA_HEADER_TO_SIGN_PREFIX_SYSTEM):
                v = headers.get(k)
                temp_headers.append(k)
                temp_headers.append(":")
                temp_headers.append(str(v))
                temp_headers.append(constant.LF)
                signature_headers.append(k)
        headers[SystemHeader.X_CA_SIGNATURE_HEADERS] = constant.SPE1.join(signature_headers)
    return ''.join(temp_headers)


def _is_header_to_sign(header_name: str, sign_headers: list) -> bool:
    """
    Http头是否参与签名 return
    :param header_name:
    :param sign_headers:
    :return:
    """
    if not header_name:
        return False
    if header_name.startswith(constant.CA_HEADER_TO_SIGN_PREFIX_SYSTEM):
        return True
    if sign_headers:
        return header_name in sign_headers
    return False
