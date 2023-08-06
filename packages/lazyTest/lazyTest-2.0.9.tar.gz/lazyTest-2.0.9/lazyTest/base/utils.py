# -*- coding = UTF-8 -*-
# Author   : xingHeYang
# time     : 2021/11/30 21:38
# ---------------------------------------
import functools


import lazyTest


def _retrying(func):
    @functools.wraps(func)
    def inner(*args):
        lazyTest.logger.debug(f"receive element selector : {args[1]}")
        if isinstance(args[1], str):
            lazyTest.logger.debug(f"{args[1]} type is str not retry")
            result = func(*args)
            return result
        lazyTest.logger.debug(f"type is list init retry config {args[1]}")
        ele = iter(args[1])
        def run(ele, *args):
            args = list(args)  # 兼容多个参数
            try:
                e = next(ele)
                lazyTest.logger.debug(f"attempt location {e}")
            except StopIteration:
                lazyTest.logger.error(f"locate retry failed")
                raise Exception(f"element retry close can not locate: {args}")
            try:
                args[1] = e  # 处理时只处理第一个参数
                result = func(*args)
                return result
            except BaseException:  # 捕获所有异常
                lazyTest.logger.debug("----------------------------- element next -----------------------------")
                result = run(ele, *args)
            return result

        result = run(ele, *args)
        return result

    return inner


def Retrying(num: int = 2):
    """
    操作执行重试，默认重试3次，3次后依然报错则判断失败
    :param num: 默认重试次数3
    :return: 无
    """

    def retrying(func):
        nonlocal num

        @functools.wraps(func)
        def inner(*args, **kwargs):
            nonlocal num
            lazyTest.logger.debug(f"action retry init retry num :{num}")

            @lazyTest.Sleep(1)
            def run(num, *args, **kwargs):
                lazyTest.logger.debug(f"action retry this is :{num} num")
                try:
                    result = func(*args, **kwargs)
                    return result
                except BaseException:
                    if num == 0:
                        lazyTest.logger.error(f"action retry failed ")
                        lazyTest.logger.debug("-----------------------------  end  -----------------------------")
                        raise Exception("action retry close can not locate")
                    lazyTest.logger.debug("----------------------------- action next -----------------------------")
                    num -= 1
                    run(num, *args, **kwargs)

            result = run(num, *args, **kwargs)
            return result

        return inner

    return retrying

def lazyLog(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        lazyTest.logger.debug("----------------------------- ready -----------------------------")
        result = func(*args,**kwargs)
        lazyTest.logger.debug("---------------------------  success  ---------------------------")
        return result
    return inner