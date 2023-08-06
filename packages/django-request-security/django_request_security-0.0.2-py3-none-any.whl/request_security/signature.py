"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/14 4:39 下午
"""
import json.decoder
import re
import hashlib

import logging

from datetime import datetime
from urllib.parse import unquote

from django.core.cache import cache

from request_security.settings import (
    SIGNATURE_METHOD,
    SIGNATURE_SECRET,
    SIGNATURE_ALLOW_TIME_ERROR,
    NONCE_CACHE_KEY,
    SIGNATURE_PASS_URL,
    SIGNATURE_DEBUG,
    SIGNATURE_PASS_URL_REGULAR
)

DELETE_KEY_MAP = [[], {}, None, '']

logger = logging.getLogger("default")


def get_sign(parameters):
    # MD5加密
    m = hashlib.md5()
    m.update(parameters)
    return m.hexdigest()


def signature_parameters(nonce: str, parameters: list):
    parameters_str = ''.join(re.findall(r"[A-Za-z0-9]", "".join(parameters) + SIGNATURE_SECRET)) + \
                     nonce
    # 参数名ASCII码从小到大排序
    parameters_sort = "".join(sorted(list(parameters_str))).split("_")
    parameters_sort[0], parameters_sort[1] = parameters_sort[1], parameters_sort[0]
    return "".join(parameters_sort).encode('UTF-8')



def check_pass_url_regular(path):
    for r in SIGNATURE_PASS_URL_REGULAR:
        if re.search(r, path):
            return True

    return False


class Log:

    def __init__(self, debug=False):
        self.debug = debug
        self.prefix = "#MIDDLEWARE# request_sign -> "

    def info(self, message):
        if self.debug:
            logger.info(self.prefix + message)

    def error(self, message):
        if self.debug:
            logger.error(self.prefix + message)

    def warning(self, message):
        if self.debug:
            logger.warning(self.prefix + message)


log = Log(debug=SIGNATURE_DEBUG)


def check_signature(request):
    """
    检查签名是否符合
    """
    if request.method.lower() not in SIGNATURE_METHOD or \
            request.path in SIGNATURE_PASS_URL or \
            check_pass_url_regular(request.path):
        return True

    timestamp = request.META.get("HTTP_T")
    nonce = request.META.get("HTTP_N")
    sign = request.META.get("HTTP_S")
    request.debug = {
        "message": 'success',
        "nonce": False,
        "timestamp": False,
        "sort": None,
        "parameters": None,
        "sign": None
    }

    log.info(("timestamp, nonce, sign=[%s, %s, %s]" % (timestamp, nonce, sign)))

    if not all([timestamp, nonce, sign]):
        log.error('required parameter missing, no pass')
        request.debug['message'] = "required parameter missing, no pass"
        return False

    # 判断cache是否正常
    if hasattr(cache, 'get') and hasattr(cache, 'set'):
        if cache.get(NONCE_CACHE_KEY.format(nonce=nonce)):
            log.error("nonce:%s repeat, no pass" % nonce)
            request.debug['message'] = "nonce:%s repeat, no pass" % nonce
            return False
        else:
            cache.set(NONCE_CACHE_KEY.format(nonce=nonce), True, 300)
            request.debug['nonce'] = True
    try:
        timestamp = int(timestamp)
    except:
        log.error("timestamp format error, no pass")
        return False

    now_timestamp = datetime.now().timestamp()
    if (now_timestamp - SIGNATURE_ALLOW_TIME_ERROR) > timestamp or timestamp > (
            now_timestamp + SIGNATURE_ALLOW_TIME_ERROR):
        log.error("request timestamp expired, not pass")
        return False
    else:
        request.debug['timestamp'] = True

    get_parameters = request.GET.dict()
    post_parameters = request.POST.dict()
    try:
        body_parameters = json.loads(request.body.decode("utf-8")) if request.body else None
    except json.decoder.JSONDecodeError:
        body_parameters = None
    log.info(
        "get_parameters, post_parameters, body_parameters=[%s, %s, %s]" % (
            get_parameters, post_parameters, body_parameters
        )
    )
    parameters = handle_parameter(
        get_parameters,
        post_parameters,
        body_parameters,
        str(timestamp)
    )
    log.info("after parameters process: %s" % parameters)
    request.debug['parameters'] = parameters
    parameters_sort = signature_parameters(nonce, parameters)
    request.debug['sort'] = parameters_sort
    result = get_sign(parameters_sort)
    request.debug['sign'] = result
    log.info("get sign:%s, origin:%s -> %s" % (
        result, sign, result == sign
    ))
    return sign == result


def handle_parameter(get_parameters, post_parameters, body_parameters, timestamp) -> list:
    parameter_list = []
    for p in [get_parameters, post_parameters, body_parameters, timestamp]:
        if isinstance(p, dict):
            t = {}
            for key, value in p.items():
                if value not in DELETE_KEY_MAP:
                    t[key] = value
            parameter_list.append(json.dumps(t, ensure_ascii=False))
        elif isinstance(p, str):
            parameter_list.append(unquote(p))
        elif isinstance(p, bytes):
            parameter_list.append(str(p, encoding="utf-8"))
    return parameter_list
