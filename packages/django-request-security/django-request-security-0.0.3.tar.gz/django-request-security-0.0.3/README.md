## django-request-security

对django请求进行签名效验

### 安装

`pip install django-request-security`

### 使用

将 `request_security.middleware.RequestSignMiddleware` 放置到中间件第一位

``` python
# django settings
MIDDLEWARE = [
    'request_security.middleware.RequestSignMiddleware',
    ...
    ...
]
```

### 前端支持与示例

需要在header头中增加的参数，这里以[axios](./example/axios/index.js)作为参考,前端签名参考[示例js文件](./example/sign/index.js)

实际使用前请不要忘了删除示例文件中输出的日志信息


| 参数  | 说明  |
| ------------ | ------------ |
| timestamp  | 请求时间戳  |
| nonce  |  请求ID（随机生成） |
| sign | 本次请求签名 |


### 配置参数

 配置参数  | 说明 | 类型 | 默认值 | 示例
------------ | ------------ | ------------ | ------------ |------------ 
  SIGNATURE_DEBUG |开启DEBUG调试| Boolean |`False`| `True`/`False`
  ENABLE_REQUEST_SIGNATURE |是否开启| Boolean |`False`| `True`/`False`
  SIGNATURE_SECRET |签名秘钥| Str|`None`|`e6QGz7AhFzFAFsR9jYoCUnZGsqDrQI`
  SIGNATURE_ALLOW_TIME_ERROR|允许请求时间前后误差|Int|`600`|`600`
  SIGNATURE_RESPONSE|签名不通过返回方法|Str|`request_security.utils.default_response`|`you_project.you_app.file.function`
  SIGNATURE_PASS_URL|不需要验证签名的url|List|[]|`['/api/v1/mcn/content/download']`
  SIGNATURE_PASS_URL_REGULAR|不需要验证签名的url正则|List|[]|`['/app/*']`
  SIGNATURE_METHOD|效验请求类型|List|['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']|['get']
  NONCE_CACHE_KEY|唯一性检查缓存key名称|Str|"django_request_security_nonce_{nonce}"|"test_{nonce}"
  
##### 参数说明：SIGNATURE_RESPONSE

```python
from django.http import HttpResponse

# request_security.utils.default_response
def default_response():
    """
        Must return django HttpResponse type
    :return: HttpResponse
    """
    return HttpResponse()
```

`request_security.utils.default_response` 方法默认返回http状态码为200的空信息，你可以自行实现一个返回函数，更改 `SIGNATURE_RESPONSE`配置
即可，但请一定注意，自行实现的函数一定要返回一个django的`HttpResponse`对象，否则django会异常。

##### 参数说明：SIGNATURE_PASS_URL


##### 参数说明：NONCE_CACHE_KEY
传入的key名称会以format函数解析，所以你必须在字符串中包括`{nonce}`
请求唯一性检查需要设置django-redis，每次请求都会插入一个key来判断唯一性，如果没有安装django-redis则此配置无效

### 忽略签名校验

部分场景(如提供api供前端下载文件)不希望某个接口或部分接口效验签名，有三种方法

#### 1. 设置参数 SIGNATURE_PASS_URL
```python
SIGNATURE_PASS_URL=['/api/v1/mcn/content/download', 'DownloadContent']
```
在此名单中的请求地址将不会效验签名，如`http://example.com/a/b/c?p=1` 填写：`/a/b/c`即可，主机与请求参数不用填写

1. 在urls.py中配置name属性 `re_path('content/download', views.DownloadContent.as_view(), name='DownloadContent')`
2. 直接写url(不推荐)

#### 2. 设置参数 SIGNATURE_PASS_URL_REGULAR
```python
SIGNATURE_PASS_URL_REGULAR=['/api/v1/*']
```

将不检查以此正则为开头的接口

#### 3. 【推荐】在View或ApiView中设置参数 ignore_sign_method

```python
class TestApi(ApiView):
    ignore_sign_method = ['get']

    def get(self, request):
        return HttpResponse()
```
将忽略此函数get方法效验

### 调试

在初期进行调试无疑是最痛苦的阶段，你可以将参数`SIGNATURE_DEBUG`设置为`True`，在后端将会打印处理参数的日志，并且在request响应时增加对应的header头信息，提供信息如下

```
Access-Control-Allow-Origin: *
allow: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS
connection: close
content-language: zh-hans
content-length: 83
content-type: application/json
Date: Thu, 16 Dec 2021 08:40:44 GMT

## 新增以下header
sign-1.nonce: True  # 重复性校验是否通过
sign-2.timestamp: True   # 时间是否在允许的范围内
sign-3.parameters: ['{"date": "2024", "_t": "1639644044077"}', '{}', '1639644044']    # 后端获取的参数
sign-4.sort: abbcddefiiijklllmopqqrttttuvvwxz000000111222333334444444445556666778899CDDFFGGHIORUWWXY    # 后端针对参数的排序
sign-5.result: d0553947cd518c47395db219ec430270     # 后端获得的签名
sign-message: success       # 提示信息，如果是不通过，这里会显示具体原因
```

### 参考

* https://www.jianshu.com/p/ad410836587a
* https://www.cnblogs.com/yoyoketang/p/11742187.html

