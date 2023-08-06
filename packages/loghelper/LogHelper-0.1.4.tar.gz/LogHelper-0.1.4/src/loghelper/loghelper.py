#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "ITXiaoPang"
__mtime__ = "2021/07/10"
__project__ = "LogHelper"
__file__ = "loghelper.py"
__IDE__ = "PyCharm"

import logging
import os
import traceback

try:
    from concurrent_log import ConcurrentTimedRotatingFileHandler as TimedRotatingFileHandler
except ImportError:
    from logging.handlers import TimedRotatingFileHandler

try:
    from flask import has_request_context, request
except ImportError:
    def has_request_context():
        return False


    class _MockFlaskRequest:
        url = 'mock_url'
        remote_addr = 'mock_remote_addr'


    request = _MockFlaskRequest()

try:
    from pythonjsonlogger.jsonlogger import JsonFormatter

    use_json_format = True
except ImportError:
    class JsonFormatter:
        def __init__(self, *args, **kwargs):
            pass


    use_json_format = False


class LogHelper:
    def __init__(self, log_dir: str, log_path: str = '/var/log/'):
        self.logging_directory = os.path.join(log_path, log_dir)
        if os.path.exists(self.logging_directory):
            if not os.path.isdir(self.logging_directory):
                raise ValueError(f'{self.logging_directory}不是目录')
        else:
            try:
                os.makedirs(self.logging_directory,mode=0o755)
            except Exception as ex:
                raise OSError(f'自动创建日志目录失败:{ex}')

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
            else:
                record.url = '-'
                record.remote_addr = '127.0.0.1'

            return super().format(record)

    logging_format = RequestFormatter(
        '<%(asctime)s> %(levelname)s '
        '(%(filename)s %(funcName)s %(lineno)d) '
        '{%(process)d %(thread)d %(threadName)s} '
        '[%(url)s %(remote_addr)s] '
        '%(message)s'
    )

    @staticmethod
    def _create_stream_handler(formatter):
        log_stream_handler = logging.StreamHandler()
        log_stream_handler.setFormatter(formatter)
        return log_stream_handler

    def _create_timed_rotating_file_handler(self, filename, formatter):
        timed_rotating_file_handler = TimedRotatingFileHandler(
            filename=os.path.join(self.logging_directory, f'{filename}.Runtime.log'),
            when='midnight', backupCount=30,
            encoding='UTF-8'
        )
        timed_rotating_file_handler.setFormatter(formatter)
        return timed_rotating_file_handler

    def create_logger(
            self, name=__name__, filename: str = __name__,
            add_stream_handler: bool = False,
            json_ensure_ascii: bool = False,
            reserved_attrs: list = None,
    ):
        _logger = logging.getLogger(name)
        _logger.setLevel(logging.INFO)
        if add_stream_handler:
            _logger.addHandler(
                self._create_stream_handler(formatter=self.logging_format)
            )
        _logger.addHandler(
            self._create_timed_rotating_file_handler(
                filename=f'raw_{filename}',
                formatter=self.logging_format
            )
        )
        if use_json_format:
            if not reserved_attrs:
                reserved_attrs = [
                    'msg',
                    'args',
                    'levelno',
                    'relativeCreated',
                ]
            logging_format_json = JsonFormatter(
                timestamp=True,
                json_indent=None,
                json_ensure_ascii=json_ensure_ascii,
                reserved_attrs=reserved_attrs
            )
            _logger.addHandler(
                self._create_timed_rotating_file_handler(
                    filename=f'json_{filename}',
                    formatter=logging_format_json
                )
            )
        return _logger

    @staticmethod
    def get_caller_frame(level: int = 3):
        ret_caller = None
        extract_stack = traceback.extract_stack()
        if len(extract_stack) > level:
            caller = extract_stack[-level]
            if isinstance(caller, traceback.FrameSummary):
                ret_caller = caller
        return ret_caller
