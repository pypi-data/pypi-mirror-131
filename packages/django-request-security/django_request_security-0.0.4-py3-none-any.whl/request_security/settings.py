from django.conf import settings

__all__ = [
    'ENABLE_REQUEST_SIGNATURE',
    'SIGNATURE_SECRET',
    'SIGNATURE_ALLOW_TIME_ERROR',
    'SIGNATURE_RESPONSE',
    'SIGNATURE_PASS_URL',
    'SIGNATURE_PASS_URL_REGULAR',
    'SIGNATURE_METHOD',
    'NONCE_CACHE_KEY',
    'SIGNATURE_DEBUG'
]

http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

SIGNATURE_DEBUG = settings.SIGNATURE_DEBUG if \
    hasattr(settings, 'SIGNATURE_DEBUG') else False

ENABLE_REQUEST_SIGNATURE = settings.ENABLE_REQUEST_SIGNATURE if \
    hasattr(settings, 'ENABLE_REQUEST_SIGNATURE') else False  # 开启签名校检

SIGNATURE_SECRET = settings.SIGNATURE_SECRET if \
    hasattr(settings, 'SIGNATURE_SECRET') else None  # 私钥

SIGNATURE_ALLOW_TIME_ERROR = settings.SIGNATURE_ALLOW_TIME_ERROR if \
    hasattr(settings, 'SIGNATURE_ALLOW_TIME_ERROR') else 600  # 允许时间误差

SIGNATURE_RESPONSE = settings.SIGNATURE_RESPONSE if \
    hasattr(settings, 'SIGNATURE_RESPONSE') else 'request_security.utils.default_response'  # 签名不通过返回方法

SIGNATURE_PASS_URL = settings.SIGNATURE_PASS_URL if \
    hasattr(settings, 'SIGNATURE_PASS_URL') else []  # 不效验签名的url

SIGNATURE_PASS_URL_REGULAR = settings.SIGNATURE_PASS_URL_REGULAR if \
    hasattr(settings, 'SIGNATURE_PASS_URL_REGULAR') else []  # 不效验签名url正则

SIGNATURE_METHOD = settings.SIGNATURE_METHOD if \
    hasattr(settings, 'SIGNATURE_METHOD') else http_method_names  # 检查的请求类型，默认全部检查

NONCE_CACHE_KEY = settings.NONCE_CACHE_KEY if \
    hasattr(settings, 'NONCE_CACHE_KEY') else "django_request_security_nonce_{nonce}"  # 检查的请求类型，默认全部检查
