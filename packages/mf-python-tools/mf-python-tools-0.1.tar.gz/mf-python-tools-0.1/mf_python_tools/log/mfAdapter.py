import logging
from .loggers import clientLogger

class mfAdapter(logging.LoggerAdapter):

    def __init__(self, logger, extra=None, source=None, host=None, source_random=None) -> None:
        """扩展logger类
            logger          logger示例
                            import loggging
                            from mf_python_tools import log_init,JSONLOGFormatter,mfAdapter
                            log_init()
                            logger = mfAdapter(logging.getLogger(__name__))
                            logger.info('this is example',event='init')
            source          日志来源
            host            日志主机字段
            source_random   是否随机source_id，True or False
        """
        super(mfAdapter, self).__init__(logger, extra or {})
        self.source= source
        self.source_random= source_random
        self.host = host
        self.client = clientLogger(source, host, source_random)

    def debug(self, msg, *args, event=None, source=None, source_id=None, source_random=None, host=None, data=None, **kwargs):
        """debug
        """
        kwargs = self.client.handle(kwargs, event, source, source_id, source_random, host, data)
        super(mfAdapter, self).debug(msg, *args, **kwargs)

    def info(self, msg, *args, event=None, source=None, source_id=None, source_random=None, host=None, data=None, **kwargs):
        kwargs = self.client.handle(kwargs, event, source, source_id, source_random, host, data)
        super(mfAdapter, self).info(msg, *args, **kwargs)

    def warning(self, msg, *args, event=None, source=None, source_id=None, source_random=None, host=None, data=None, **kwargs):
        kwargs = self.client.handle(kwargs, event, source, source_id, source_random, host, data)
        super(mfAdapter, self).warning(msg, *args, **kwargs)

    def warn(self, msg, *args, event=None, source=None, source_id=None, source_random=None, host=None, data=None, **kwargs):
        kwargs = self.client.handle(kwargs, event, source, source_id, source_random, host, data)
        super(mfAdapter, self).warn(msg, *args, **kwargs)

    def error(self, msg, *args, event=None, source=None, source_id=None, source_random=None, host=None, data=None, **kwargs):
        kwargs = self.client.handle(kwargs, event, source, source_id, source_random, host, data)
        super(mfAdapter, self).error(msg, *args, **kwargs)

    def exception(self, msg, *args, event=None, source=None, source_id=None, source_random=None, host=None, data=None, exc_info=True, **kwargs):
        kwargs = self.client.handle(kwargs, event, source, source_id, source_random, host, data)
        super(mfAdapter, self).exception(msg, *args, exc_info, **kwargs)

    def critical(self, msg, *args, event=None, source=None, source_id=None, source_random=None, host=None, data=None, **kwargs):
        kwargs = self.client.handle(kwargs, event, source, source_id, source_random, host, data)
        super(mfAdapter, self).critical(msg, *args, **kwargs)
