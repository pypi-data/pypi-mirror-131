# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['loghelper']

package_data = \
{'': ['*']}

extras_require = \
{'concurrent': ['concurrent-log>=1.0,<2.0'],
 'flask': ['Flask>=2.0,<3.0'],
 'json': ['python-json-logger>=2.0,<3.0']}

setup_kwargs = {
    'name': 'loghelper',
    'version': '1.0.1',
    'description': '日志助手，支持多进程，支持json格式，支持flask',
    'long_description': '# 日志助手\n\n## 特性\n1. 几乎无需配置，就可生成日志文件\n2. 可选，输出到文件的同时打印到屏幕\n3. 可选（安装python-json-logger即可），生成纯文本日志的同时生成一份json格式的日志，方便采集\n4. 可选（安装flask即可），捕获flask的remote_addr和url信息\n5. 可选（安装concurrent-log），支持多进程并发记录日志\n\n```python\n# 简易用法\nfrom loghelper import LogHelper\n\nlog_helper = LogHelper(log_dir=\'my_project\', log_path=\'/tmp/\')\n\nlogger = log_helper.create_logger()\n\nlogger.info(\'Hello World\')\n```\n\n```python\n# 完整用法\nfrom loghelper import LogHelper\n\nlog_helper = LogHelper(log_dir=\'my_project\', log_path = \'/var/log/\', backup_count=7)\n\nlogger = log_helper.create_logger(\n    name=\'my_module\',\n    filename=\'my_module\',\n    add_stream_handler = True,\n    json_ensure_ascii = False,\n    reserved_attrs = [\n        \'msg\',\n        \'args\',\n        \'levelno\',\n        \'relativeCreated\',\n    ]\n)\n\nlogger.info(\'Hello World\')\n```\n\n## 生成日志样例\n### 纯文本\n/tmp/my_project/raw_loghelper.loghelper.Runtime.log\n```text\n<2021-12-15 14:40:38,844> INFO (<stdin> <module> 1) {13064 4474015232 MainThread} [- 127.0.0.1] Hello World\n```\n### json\n/tmp/my_project/json_loghelper.loghelper.Runtime.log\n```json\n{"message": "Hello World", "name": "loghelper.loghelper", "levelname": "INFO", "pathname": "<stdin>", "filename": "<stdin>", "module": "<stdin>", "exc_info": null, "exc_text": null, "stack_info": null, "lineno": 1, "funcName": "<module>", "created": 1639550438.844173, "msecs": 844.1729545593262, "thread": 4474015232, "threadName": "MainThread", "processName": "MainProcess", "process": 13064, "url": "-", "remote_addr": "127.0.0.1", "asctime": "2021-12-15 14:40:38,844", "timestamp": "2021-12-15T06:40:38.844173+00:00"}\n```\n',
    'author': 'ITXiaoPang',
    'author_email': 'itxiaopang.djh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
