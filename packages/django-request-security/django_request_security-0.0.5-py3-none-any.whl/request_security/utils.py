"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/16 4:52 下午
"""

from django.http import HttpResponse


def default_response():
    """
        Must return django HttpResponse type
    :return: HttpResponse
    """
    return HttpResponse()
