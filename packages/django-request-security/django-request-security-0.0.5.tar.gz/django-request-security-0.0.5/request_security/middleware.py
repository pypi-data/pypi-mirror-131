"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/7/30 4:42 下午
"""
from typing import Optional
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.module_loading import import_string

from request_security.signature import check_signature, log
from request_security.settings import SIGNATURE_RESPONSE, ENABLE_REQUEST_SIGNATURE, SIGNATURE_DEBUG

DEBUG_HEADER_MAP = {
    'sign-message': 'message',
    'sign-1.nonce': 'nonce',
    'sign-2.timestamp': 'timestamp',
    'sign-3.parameters': 'parameters',
    'sign-4.sort': 'sort',
    'sign-5.result': 'sign'
}

DEBUG_HEADER_MAX_LENGTH = 512


def set_debug_header(request, response):
    if hasattr(request, 'debug') and isinstance(request.debug, dict):
        for item in DEBUG_HEADER_MAP:
            if len(str(request.debug.get(DEBUG_HEADER_MAP[item], ''))) > DEBUG_HEADER_MAX_LENGTH:
                value = 'pass set debug header, data too large.'
            else:
                value = request.debug.get(DEBUG_HEADER_MAP[item])
            response.setdefault(item, value)


class RequestSignMiddleware(MiddlewareMixin):

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs) -> Optional[HttpResponse]:
        if ENABLE_REQUEST_SIGNATURE:
            # check view settings
            ignore_sign_method = getattr(view_func.cls, 'ignore_sign_method', [])
            if not isinstance(ignore_sign_method, list):
                log.warning(
                    'function: %s parameter: ignore_sign_method will not take effect, type must list, not %s' % (
                        view_func.__name__, type(ignore_sign_method)
                    )
                )
                ignore_sign_method = []
            if ignore_sign_method and \
                    request.method.lower() in ignore_sign_method:
                return None
            # check sign
            if not check_signature(request):
                response = import_string(SIGNATURE_RESPONSE)(request)
                if SIGNATURE_DEBUG:
                    set_debug_header(request, response)
                return response

    @staticmethod
    def process_response(request, response):
        # ignore_sign_method not have debug attr
        if hasattr(request, 'debug') and SIGNATURE_DEBUG:
            set_debug_header(request, response)
        return response
