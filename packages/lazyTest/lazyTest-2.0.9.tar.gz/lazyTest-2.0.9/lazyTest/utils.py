# -*- coding = UTF-8 -*-
# Author   : buxiubuzhi
# Project  : lazyTest
# FileName : utils.py
# Describe :
# ---------------------------------------

import os
import time
import functools

import lazyTest


def Sleep(s: float = 0.5):
    """
    每个操作执行前后强制休眠。默认0.5
    """

    def Sleep(func):
        nonlocal s

        @functools.wraps(func)
        def inner(*args, **kwargs):
            time.sleep(s)
            result = func(*args, **kwargs)
            time.sleep(s)
            return result

        return inner

    return Sleep


def getPorjectPath():
    """
    获取项目路径
    """
    return os.path.dirname(os.path.dirname(__file__))


def ClearTestResult(path: str):
    """
    清空指定目录下所有文件
    :param path: 指定目录清空
    :return: 无
    """
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            ClearTestResult(path_file)


def clearLogAndReport(ProjectPath):
    """
    清空上次执行的记录
    :param ProjectPath: 项目根目录，根据项目根目录查找result目录进行清空
    :return: 无
    """

    def clear(func):
        nonlocal ProjectPath

        @functools.wraps(func)
        def inner(*args, **kwargs):
            lazyTest.logger.debug("----------清空上次测试结果----------")
            path = ProjectPath + "/result"
            ClearTestResult(path)
            result = func(*args, **kwargs)
            return result

        return inner

    return clear

