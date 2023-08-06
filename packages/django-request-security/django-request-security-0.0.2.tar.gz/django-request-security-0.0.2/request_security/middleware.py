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


def set_debug_header(request, response):
    response.setdefault('sign-message', request.debug.get('message'))
    response.setdefault('sign-1.nonce', request.debug.get('nonce'))
    response.setdefault('sign-2.timestamp', request.debug.get('timestamp'))
    response.setdefault('sign-3.parameters', request.debug.get('parameters'))
    response.setdefault('sign-4.sort', request.debug.get('sort'))
    response.setdefault('sign-5.result', request.debug.get('sign'))


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
        if SIGNATURE_DEBUG:
            set_debug_header(request, response)
        return response
