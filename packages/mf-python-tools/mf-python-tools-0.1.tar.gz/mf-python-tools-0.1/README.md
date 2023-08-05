# mf-python-tools
MF some tools for Python

## 安装

`pip install mf-python-tools`

## jsonr日志

### 说明

#### 使用mfAdapter
```
import logging
from mf_python_tools import log_init,JSONLOGFormatter,mfAdapter

log_init()

logger = mfAdapter(logging.getLogger(__name__))

logger.info('this is log..',event='log.init')

## {"datetime": "2021-12-10T04:00:52.952", "source_id": "", "source": "", "host": "fsy-work", "level": "INFO", "event": "log.init", "file_line": "/server/mf-python-tools/mf_python_tools/log/mfAdapter.py info: 8", "msg": "logger this is info........", "data": {}}
```

#### 准确定位行数

```
import logging
from mf_python_tools import log_init,JSONLOGFormatter,clientLogger

log_init()

logger = logging.getLogger(__name__)
# print
mlog = clientLogger(source_random=True)

 md = mlog.data('app init.','fffffff',event="app.init",aa="bbb",source="aaa",data=['ddd','cccc'],extra={"abc":"dddddffff","data":{"cccc":"sss","mf":['aaa','bbb']}})
logger.info(md[0],*md[1],**md[2])

## {"datetime": "2021-12-10T07:52:35.296", "source_id": "ym0LlQDBCHuGFYSt07FurrU2RQSEnTr1", "source": "aaa", "host": "fsy-work", "level": "INFO", "event": "app.init", "file_line": "/mnt/sdb/tmp/cementTest/cementtest/main.py main: 169", "msg": "app init.", "abc": "dddddffff", "aa": "bbb", "data": ["ddd", "cccc", ["app init.", "fffffff"]]}
```

#### 使用logging

```
from mf_python_tools import log_init,clientLogger,mfAdapter,LOG_DEFAULT_CONFIG
logging.config.dictConfig(LOG_DEFAULT_CONFIG)
logger = logging.getLogger(__name__)

logger.info('ddddddddddddddddddddddddddddddddddd','mmmmm',extra={'event':'celery.app.init','data':{"aaaa":'11111','bbb':'dddd'}})

## {"datetime": "2021-12-13T07:59:14.690", "source_id": "", "source": "", "host": "fsy-work", "level": "INFO", "event": "celery.app.init", "file_line": "/mnt/sdb/tmp/testCeleryLog/app.py <module>: 29", "msg": "ddddddddddddddddddddddddddddddddddd", "data": {"aaaa": "11111", "bbb": "dddd", "msg_ext": ["ddddddddddddddddddddddddddddddddddd", "mmmmm"]}}

```

### 说明

#### LOG_DEFAULT_CONFIG

```

LOG_DEFAULT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '{"datetime": "%(asctime)s", "host": ""'
                      '"source": "", "level": "%(levelname)s", '
                      '"source_id": "", "event": "", '
                      '"file_line": "%(pathname)s %(funcName)s: %(lineno)d", '
                      '"msg": "%(message)s"}'

        },
        'json': {
            'class': 'mf_python_tools.JSONLOGFormatter'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.StreamHandler'
        },
        'consoleJson': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'json',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'access.log',
            'when': 'D',
            'backupCount': 31,
        },
        'fileError': {
            'level': 'WARNING',
            'formatter': 'json',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'error.log',
            'when': 'D',
            'backupCount': 31,
        },
    },
    'loggers': {
        '': {
            'handlers': ['consoleJson'],
            'level': 'INFO',
            'propagate': False,
        },
        'tasks': {
            'handlers': ['consoleJson','file','fileError'],
            'level': 'INFO',
            'propagate': False,
        },
        'cement': {
            'handlers': ['consoleJson','file','fileError'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['consoleJson','file','fileError'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    "root": {
            'handlers': ['consoleJson'],
            'level': 'DEBUG',
            'propagate': False,
    }
}

```


#### log_init
配置初始化

#### 其他方法

- add_handlers： 为配置项添加一个handler，需要在log_init之前调用
  - name： handlers名称，如果存在则添加失败
  - default: 是否采用默认配置，True or False
    ```
    {
        'level': 'INFO',
        'formatter': 'json',
        'class': 'logging.StreamHandler',
    }
    ```
  - data: 自定义数据
    ```
    {
        'level': 'INFO',
        'formatter': 'json',
        'class': 'logging.StreamHandler',
    }
    ```

- add_loggers： 为配置项添加一个loggers，需要在log_init之前调用
  - name： handlers名称，如果存在则添加失败
  - default: 是否采用默认配置，True or False
    ```
    {
        "handlers": ["consoleJson"],
        "level": "INFO",
        "propagate": False,
    }
    ```
  - data: 自定义数据
    ```
    {
        "handlers": ["consoleJson"],
        "level": "INFO",
        "propagate": False,
    }
    ```

#### update_handlers,update_loggers
更新handler,logger

#### get_log_config
获取配置

#### JSONLOGFormatter
logging.Formatter实现类
数据个刷成json字符串

#### clientLogger
数据组装

##### 参数

- source： 打印的数据源字段，None or ''
- host:    打印的主机名,None
- source_random  如果不传入source_id,是否自动产生source_id, None or Ture of False

#### mfAdapter
logger类扩展类，打印数据

##### 参数

- source： 打印的数据源字段，None or ''
- host:    打印的主机名,None
- source_random  如果不传入source_id,是否自动产生source_id, None or Ture of False
