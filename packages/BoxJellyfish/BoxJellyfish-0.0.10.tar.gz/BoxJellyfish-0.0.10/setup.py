#!/usr/bin/env python

from setuptools import setup, find_packages

# 第三方依赖
requires = [
    "six"
]

# 导入静态文件
file_data = [
    ("bjf/static/", ["bjf/data.csv"]),
]

setup(
    name='BoxJellyfish',
    version='0.0.10',
    keywords=('deploy', 'egg', 'ai'),
    description='Automated deployment platform',
    license='MIT License',

    url='http://www.baidu.com',
    author='LongGengYong',
    author_email='yonglonggeng@163.com',

    packages=find_packages(),
    include_package_data=True,
    platforms='linux',
    install_requires=requires,
    zip_safe=False,
    data_files=file_data,
)

