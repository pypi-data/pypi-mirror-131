# -*- coding = UTF-8 -*-
# Author   : xingHeYang
# time     : 2021/11/29 21:13
# ---------------------------------------
import logging

from loguru import logger


class PropogateHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        logging.getLogger(record.name).handle(record)


logger.add(PropogateHandler(), format="{time:YYYY-MM-DD HH:mm:ss} | {message}")
