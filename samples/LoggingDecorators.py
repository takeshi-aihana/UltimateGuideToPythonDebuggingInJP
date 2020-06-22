#!/usr/bin/env python3
# -*- mode:python; coding: utf-8 -*-
#
# 
#
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#--------+---------+---------+---------+---------X---------+---------+---------+

from functools import wraps, partial
import logging
import sys

def attach_wrapper(obj, func=None):    # 任意のオブジェクトの属性として関数を接続するヘルパー関数
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func

def log(level, message):               # 実際のデコレータ
    def decorate(func):
        logger = logging.getLogger(func.__module__)        # ロガーを取得する
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        log_message = f'{func.__name__} - {message}'

        @wraps(func)
        def wrapper(*args, **kwargs):  # デコレートする関数を実行する前にメッセージをログする
            logger.log(level, log_message)
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)       # 属性として set_level() を wrapper() に接続する
        def set_level(new_level):      # ログのレベルをセットする関数
            nonlocal level
            level = new_level

        @attach_wrapper(wrapper)       # 属性として set_message() を wrapper() に接続する
        def set_message(new_message):  # ログのメッセージをセットする関数
            nonlocal log_message
            log_message = f'{func.__name__} - {new_message}'

        return wrapper
    return decorate


# 使用例
@log(logging.WARN, 'example-param')
def somebuggyfunc(args):
    return args

def main():
    somebuggyfunc('some args')

    # 内部のデコレータ関数にアクセスしてログレベルとログメッセージを変更する
    somebuggyfunc.set_level(logging.CRITICAL)
    somebuggyfunc.set_message('new-message')
    
    somebuggyfunc('some args');

if __name__ == "__main__":
    sys.exit(main())

#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#--------+---------+---------+---------+---------X---------+---------+---------+
