
from setuptools import setup

setup(
    name='datamemorys',
    version='0.0.8',
    author='lubupang',
    author_email='lbl@rrftech.com',
    url='https://www.zhihu.com/column/c_1410908597132423168',
    description=u'数字记忆插件官方数据包',
    packages=['datamemorys','datamemorys.core','datamemorys.datas','datamemorys.reports','datamemorys.utils'],
    install_requires=['lac','pandas==1.0.0']
)