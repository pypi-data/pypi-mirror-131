# 日志助手

## 特性
1. 几乎无需配置，就可生成日志文件
2. 可选，输出到文件的同时打印到屏幕
3. 可选（安装python-json-logger即可），生成纯文本日志的同时生成一份json格式的日志，方便采集
4. 可选（安装flask即可），捕获flask的remote_addr和url信息
5. 可选（安装concurrent-log），支持多进程并发记录日志

```python
# 简易用法
from loghelper import LogHelper

log_helper = LogHelper(log_dir='my_project', log_path='/tmp/')

logger = log_helper.create_logger()

logger.info('Hello World')
```

```python
# 完整用法
from loghelper import LogHelper

log_helper = LogHelper(log_dir='my_project', log_path = '/var/log/', backup_count=7)

logger = log_helper.create_logger(
    name='my_module',
    filename='my_module',
    add_stream_handler = True,
    json_ensure_ascii = False,
    reserved_attrs = [
        'msg',
        'args',
        'levelno',
        'relativeCreated',
    ]
)

logger.info('Hello World')
```

## 生成日志样例
### 纯文本
/tmp/my_project/raw_loghelper.loghelper.Runtime.log
```text
<2021-12-15 14:40:38,844> INFO (<stdin> <module> 1) {13064 4474015232 MainThread} [- 127.0.0.1] Hello World
```
### json
/tmp/my_project/json_loghelper.loghelper.Runtime.log
```json
{"message": "Hello World", "name": "loghelper.loghelper", "levelname": "INFO", "pathname": "<stdin>", "filename": "<stdin>", "module": "<stdin>", "exc_info": null, "exc_text": null, "stack_info": null, "lineno": 1, "funcName": "<module>", "created": 1639550438.844173, "msecs": 844.1729545593262, "thread": 4474015232, "threadName": "MainThread", "processName": "MainProcess", "process": 13064, "url": "-", "remote_addr": "127.0.0.1", "asctime": "2021-12-15 14:40:38,844", "timestamp": "2021-12-15T06:40:38.844173+00:00"}
```
