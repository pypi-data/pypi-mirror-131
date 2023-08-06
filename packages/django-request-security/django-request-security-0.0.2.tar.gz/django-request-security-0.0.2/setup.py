# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/12 1:39 下午
@desc:
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-request-security",
    version="0.0.2",
    author="liyao",
    author_email="liyao2598330@126.com",
    description="third-party libraries that enhance the security of the Django API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucatisfun/django-request-security",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3',
)
